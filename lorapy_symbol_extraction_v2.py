#!/usr/bin/env python
# coding: utf-8

# # lorapy symbol extraction

# In[1]:



import pathlib

import os, sys
from loguru import logger
logger.remove(None)
logger.add(sys.stdout, colorize=True)

import numpy as np
from six.moves import cPickle
from tqdm import tqdm

import matplotlib.pyplot as plt 

logger.add('dev/lorapy-symbol-extraction-v2.log', level='DEBUG')


# In[2]:


import lorapy

import scipy as sp
import scipy.signal as spsig
import warnings
import multiprocessing
from functools import partial 

from lorapy.symbols import utils as sym_utils


# ## setup 

# In[3]:


_BASE_DATA_DIR = pathlib.Path('../data')

BENCHTOP_DATA_DIR = _BASE_DATA_DIR.joinpath('lora-benchtop-recording')
DOTP_DATA_DIR = _BASE_DATA_DIR.joinpath('symbol-ref')
DEV_DATA_DIR = _BASE_DATA_DIR.joinpath('dev-data')
PREAM_WIN_DIR = _BASE_DATA_DIR.joinpath('lora-preamble-windows-20k')


# # load

# ## dat files

# In[4]:


loader = lorapy.load_dat(BENCHTOP_DATA_DIR, autoload=True)
loader.file_list


# ## dotp files

# In[5]:


ploader = lorapy.load_dotp(DOTP_DATA_DIR)
ploader.file_list


# In[ ]:





# # process 

# ## symbol correlation settings

# In[6]:


_step_dict = {
    1: 100,
    2: 100,
    7: 4,
    8: 2,
    9: 2,
}


# ## functions

# In[ ]:





# In[7]:


def _load_matching_dotp(bw: int, sf: int):
    return ploader.filter(bw=bw, sf=sf)[0]

def _convert_files(file, dotp_file):
    return file.to_signal(), dotp_file.to_signal()


def _load_and_convert(file):
    file.load()
    dotp_file = _load_matching_dotp(file.bw, file.sf)
    
    signal, base_symbol = _convert_files(file, dotp_file)
    
    return signal, base_symbol


def _extract_and_manual_adjust(signal):
    signal.extract_packets(method='slide-mean', auto_adj=False, overlap=0.5)
    signal.adjust_packets(
        force_check=True, 
        adjust_type='biased-mean', 
        look_ahead=10, threshold=0.5,
    )
    
    return signal


def _format_output_path(base_dir, signal):
    filename = pathlib.Path(signal.stats.filename)
    
    out_path = base_dir.joinpath(
        'processed-symbols'
    ).joinpath(
        filename.with_suffix('').with_suffix('.p')
    )
    
    return out_path


def _save_symbols(data, signal, base_dir):
    out_path = _format_output_path(base_dir, signal)
    
    with out_path.open('wb') as outfile:
        cPickle.dump(data, outfile)

        
def _extract_symbols(packet):
    packet.extract_preamble_window()
    return packet._preamble_window


def _extract_and_save_symbols(packets):
    full_array = np.vstack([
        _extract_symbols(packet)
        for packet in packets
    ])
    
    packet = packets[0]
    _save_symbols(full_array, packet)
        

def _get_correlation_values(base_symbol, preamble, samp_per_sym, shift_step):
    shifts = sym_utils.generate_shifts(
        samp_per_sym, range_factor=10, step=shift_step,
    )
    
    corr_vals = sym_utils.shift_and_correlate(
        base_symbol.data, preamble, samp_per_sym, shifts,
    ) 
    
    return corr_vals

def _get_adjusted_distance(samp_per_sym, shift_step):
    distance = int(samp_per_sym // shift_step)
    distance *= 0.90 
    return distance


def _find_peaks(corr_vals, samp_per_sym, shift_step):
    adjusted_dist = _get_adjusted_distance(samp_per_sym, shift_step)
    
    peaks = spsig.find_peaks(
        corr_vals, 
        distance=adjusted_dist,
    )[0]
    
    return peaks 


def _corr_sanity_plot(corr_vals, peaks):
    symbol_strips = [
        np.max(corr_vals) * 1.1 if idx in peaks else 0
        for idx, _ in enumerate([0] * len(corr_vals))
    ]
    
    fig, axs = plt.subplots(2)
    axs[0].plot(corr_vals)
    axs[1].plot(corr_vals)
    axs[1].plot(symbol_strips)
    plt.show()

    
def _extract_symbols_from_peaks(packet_data: np.ndarray, peak_shifts: list, samp_per_sym: int) -> np.ndarray:
    symbols = np.vstack([
        packet_data[shift: shift+samp_per_sym]
        for shift in peak_shifts
    ])
    
    return symbols
        

def _sanity_plot(symbols):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig, ax = plt.subplots(symbols.shape[0])

        for idx, sym in enumerate(symbols):
            ax[idx].plot(sym)


def correlate_and_slice(packet, base_symbol, save_sanity=False):
    samp_per_sym, shift_step = packet.stats.samp_per_sym, _step_dict[packet.stats.bw]
    
    shifts = sym_utils.generate_shifts(
        samp_per_sym, range_factor=10, step=shift_step,
    )

    corr_vals = sym_utils.shift_and_correlate(
        base_symbol, packet.data, samp_per_sym, shifts,
    ) 
    
    peaks = _find_peaks(corr_vals, samp_per_sym, shift_step)
    
    shifts = list(shifts)
    peak_shifts = [shifts[peak] for peak in peaks]
    
    symbols = _extract_symbols_from_peaks(packet.data, peak_shifts, samp_per_sym)
    
    if save_sanity:
        _sanity_plot(symbols)
    
    return symbols



def slice_all_packets(packets, symbol_data):
    six_symbol_data = np.concatenate([symbol_data] * 6)
    corr_slice = partial(correlate_and_slice, base_symbol=six_symbol_data)
    
    with multiprocessing.Pool() as pool:
        results = pool.map(corr_slice, packets)
        
    return np.vstack(results)

def process_and_save(file):
    signal, base_symbol = _load_and_convert(file)
    signal = _extract_and_manual_adjust(signal)
    results = slice_all_packets(signal.packets, base_symbol.data)
    
    _save_symbols(results, signal, _BASE_DATA_DIR)
    

# ## setup



exceptioned_files = []

for file in tqdm(loader.file_list):
    logger.warning(f'working file: {file}')
    try:
        process_and_save(file)
    except Exception:
        exceptioned_files.append(file.name) 









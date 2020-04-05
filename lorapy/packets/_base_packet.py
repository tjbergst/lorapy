# base lora packet

import numpy as np
import typing as ty
from lorapy.common.stats import LoraStats  # TODO: circ import issue


class BaseLoraPacket:

    def __init__(self, data: np.array, stats: LoraStats, packet_id: int, endpoints: ty.Tuple[int, int]):

        self.data = data
        self.stats = stats
        self.pid = packet_id

        self.endpoints = endpoints


    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.pid}) || size: {self.size} | {self.stats}"

    def __len__(self):
        return self.data.size

    def __iter__(self):
        yield from self.data

    @property
    def min(self) -> float:
        return self.real_abs_data.min()

    @property
    def max(self) -> float:
        return self.real_abs_data.max()

    @property
    def mean(self) -> float:
        return self.real_abs_data.mean()

    @property
    def size(self) -> int:
        return self.data.size

    @property
    def real_abs_data(self) -> np.array:
        return np.real(np.abs(self.data))

    @property
    def adjustment(self) -> int:
        return self.stats.packet_adjustment

    @adjustment.setter
    def adjustment(self, adj: int) -> None:
        self.stats.packet_adjustment = adj

    @property
    def endpoints(self) -> ty.Tuple[int, int]:
        return self.stats.packet_endpoints

    @endpoints.setter
    def endpoints(self, _endpoints: ty.Tuple[int, int]) -> None:
        self.stats.packet_endpoints = _endpoints

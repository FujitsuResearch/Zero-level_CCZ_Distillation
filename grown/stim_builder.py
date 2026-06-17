# from __future__ import annotations
from collections import defaultdict
from copy import deepcopy

import stim

class Stim_builder:
    def __init__(self, grid_range: tuple[int, int], error_probabilities: list[float]):
        # circuit initialization
        self.circuits =  [stim.Circuit()]
        self.error_probabilities: list[float] = error_probabilities
        self.error_probabilities_num: int = len(self.error_probabilities)
        self.circuit_depths: int = 100
        self.noisy: bool = True
        self.nearest_neighbor = True
        
        # grid initialization
        self.grid_range_x: int = grid_range[0]
        self.grid_range_y: int = grid_range[1]
        self.qubit_grid_to_num: dict[tuple[int|float, int|float], int] = {}
        self.qubit_num_max: int = 0
        for i in range(self.grid_range_x):
            for j in range(self.grid_range_y):
                self.qubit_grid_to_num[(i, j)] = self.qubit_num_max
                self.qubit_num_max += 1
        for i in range(self.grid_range_x - 1):
            for j in range(self.grid_range_y - 1):
                self.qubit_grid_to_num[(i + 0.5, j + 0.5)] = self.qubit_num_max
                self.qubit_num_max += 1
                
        for key, value in self.qubit_grid_to_num.items():
            self.circuits[0].append("QUBIT_COORDS", value, key)
        
        for _ in range(self.error_probabilities_num - 1):
            self.circuits.append(deepcopy(self.circuits[0]))
        
        # variable initialization
        self.tasks = [[] for _ in range(self.circuit_depths)]
        self.idling_qubit: list[list[bool]] = [[True for i in range(self.qubit_num_max)] for j in range(self.circuit_depths)]
        self.current_depth: int = 0
        self.measurement_count: int = 0
        self.observable_count: int = 0
        self.postselect: list = []
        self.measurement_tag: dict[int, list[int]] = defaultdict(list)
    
    # test function
    def _nearest_neighbor(self, qubit1, qubit2) -> bool:
        if abs(qubit1[0] - qubit2[0]) == 0.5 and abs(qubit1[1] - qubit2[1]) == 0.5:
            return True
        return False
    
    # settings
    def ideal_start(self):
        self.noisy = False
    
    def ideal_end(self):
        self.noisy = True
        
    def nearest_neighbor_switch(self):
        self.nearest_neighbor = False

    # gate operations
    def rz(self, qubit: tuple):
        self.idling_qubit[self.current_depth][self.qubit_grid_to_num[qubit]] = False
        self.tasks[self.current_depth].append(("R", self.qubit_grid_to_num[qubit]))
        if self.noisy:
            self.tasks[self.current_depth].append(("X_ERROR", self.qubit_grid_to_num[qubit]))
            
    def rx(self, qubit: tuple):
        self.idling_qubit[self.current_depth][self.qubit_grid_to_num[qubit]] = False
        self.tasks[self.current_depth].append(("RX", self.qubit_grid_to_num[qubit]))
        if self.noisy:
            self.tasks[self.current_depth].append(("Z_ERROR", self.qubit_grid_to_num[qubit]))
    
    def mz(self, qubit: tuple, count: int|None = None):
        self.idling_qubit[self.current_depth][self.qubit_grid_to_num[qubit]] = False
        if self.noisy:
            self.tasks[self.current_depth].append(("X_ERROR", self.qubit_grid_to_num[qubit]))
        self.tasks[self.current_depth].append(("M", self.qubit_grid_to_num[qubit], count))

    def mx(self, qubit: tuple, count: int|None = None):
        self.idling_qubit[self.current_depth][self.qubit_grid_to_num[qubit]] = False
        if self.noisy:
            self.tasks[self.current_depth].append(("Z_ERROR", self.qubit_grid_to_num[qubit]))
        self.tasks[self.current_depth].append(("MX", self.qubit_grid_to_num[qubit], count))
    
    def mrz(self, qubit: tuple, count: int|None = None):
        self.idling_qubit[self.current_depth][self.qubit_grid_to_num[qubit]] = False
        if self.noisy:
            self.tasks[self.current_depth].append(("X_ERROR", self.qubit_grid_to_num[qubit]))
        self.tasks[self.current_depth].append(("MR", self.qubit_grid_to_num[qubit], count))
        if self.noisy:
            self.tasks[self.current_depth].append(("X_ERROR", self.qubit_grid_to_num[qubit]))
    
    def mrx(self, qubit: tuple, count: int|None = None):
        self.idling_qubit[self.current_depth][self.qubit_grid_to_num[qubit]] = False
        if self.noisy:
            self.tasks[self.current_depth].append(("Z_ERROR", self.qubit_grid_to_num[qubit]))
        self.tasks[self.current_depth].append(("MRX", self.qubit_grid_to_num[qubit], count))
        if self.noisy:
            self.tasks[self.current_depth].append(("Z_ERROR", self.qubit_grid_to_num[qubit]))
    
    def cnot(self, qubit1: tuple, qubit2: tuple):
        # assert self._nearest_neighbor(qubit1, qubit2)
        self.idling_qubit[self.current_depth][self.qubit_grid_to_num[qubit1]] = False
        self.idling_qubit[self.current_depth][self.qubit_grid_to_num[qubit2]] = False
        self.tasks[self.current_depth].append(("CNOT", (self.qubit_grid_to_num[qubit1], self.qubit_grid_to_num[qubit2])))
        if self.noisy:
            self.tasks[self.current_depth].append(("DEPOLARIZE2", (self.qubit_grid_to_num[qubit1], self.qubit_grid_to_num[qubit2])))
        
    def classical_cnot(self, qubit2: tuple):
        self.tasks[self.current_depth].append(("CNOT", (stim.target_rec(-1), self.qubit_grid_to_num[qubit2])))

    def classical_cz(self, qubit2: tuple):
        self.tasks[self.current_depth].append(("CZ", (stim.target_rec(-1), self.qubit_grid_to_num[qubit2])))

    # stim operations
    def tick(self):
        if self.noisy:
            for qubit_num in range(len(self.idling_qubit[self.current_depth])):
                if self.idling_qubit[self.current_depth][qubit_num]:
                    self.tasks[self.current_depth].append(("DEPOLARIZE1", qubit_num))
        self.tasks[self.current_depth].append("TICK")
                    
        self.current_depth += 1
    
    def detector(self, numbers: list, postselect: bool = False, detector: bool = False):
        self.tasks[self.current_depth].append(("DETECTOR", numbers, postselect, detector))
    
    def observable(self, numbers: tuple):
        self.tasks[self.current_depth].append(("OBSERVABLE_INCLUDE", numbers, self.observable_count))
        self.observable_count += 1
    
    def ideal(self, qubits: list[tuple]):
        for qubit in qubits:
            self.idling_qubit[self.current_depth][self.qubit_grid_to_num[qubit]] = False
    
    def _get_inverse_tag_second_last(self, tag_number:int):
        return -1 * (self.measurement_count - self.measurement_tag[tag_number][-2])

    def _get_inverse_tag(self, tag_number:int, dictnumber:int):
        return -1 * (self.measurement_count - self.measurement_tag[tag_number][dictnumber])

    # output operations
    def build(self):
        for error_prob_num in range(self.error_probabilities_num):
            self.idling_qubit: list[list[bool]] = [[True for i in range(self.qubit_num_max)] for j in range(self.circuit_depths)]
            self.current_depth: int = 0
            self.measurement_count: int = 0
            self.observable_count: int = 0
            self.postselect: list = []
            self.detector_list: list = []
            self.measurement_tag: dict[int, list[int]] = defaultdict(list)

            for task in self.tasks:
                for operation in task:
                    if operation[0] in ('R', "RX"):
                        self.circuits[error_prob_num].append(operation[0], operation[1])
                    elif operation[0] in ('M', "MX", "MR", "MRX"):
                        self.circuits[error_prob_num].append(operation[0], operation[1])
                        if operation[2] is not None:
                            self.measurement_tag[operation[2]].append(self.measurement_count)
                            # print(self.measurement_tag)
                        self.measurement_count += 1
                    elif operation[0] == "CNOT":
                        self.circuits[error_prob_num].append(operation[0], operation[1])
                    elif operation[0] == "CZ":
                        self.circuits[error_prob_num].append(operation[0], (stim.target_rec(-1), operation[1][1]))
                    elif operation[0] in ("Z_ERROR", "X_ERROR", "DEPOLARIZE1", "DEPOLARIZE2"):
                        self.circuits[error_prob_num].append(operation[0], operation[1], self.error_probabilities[error_prob_num])
                    elif operation == "TICK":
                        self.circuits[error_prob_num].append("TICK")
                    elif operation[0] == "DETECTOR":
                        tmp = []
                        for rec_num in operation[1]:
                            if type(rec_num) is int:
                                if rec_num < 0:
                                    tmp.append(rec_num)
                                else:
                                    # print(self.measurement_tag)
                                    tmp.append(self._get_inverse_tag_second_last(rec_num))
                            else:
                                # print(self.measurement_tag[rec_num[0]])
                                # print(self.measurement_tag)
                                tmp.append(self._get_inverse_tag(rec_num[0], rec_num[1]))
                        self.circuits[error_prob_num].append(operation[0], [stim.target_rec(i) for i in tmp])
                        self.postselect.append(operation[2])
                        self.detector_list.append(operation[3])
                    elif operation[0] == "OBSERVABLE_INCLUDE":
                        tmp = []
                        for rec_num in operation[1]:
                            if type(rec_num) is int:
                                if rec_num < 0:
                                    tmp.append(rec_num)
                                else:
                                    # print(self.measurement_tag)
                                    tmp.append(self._get_inverse_tag_second_last(rec_num))
                            else:
                                # print(self.measurement_tag[rec_num[0]])
                                tmp.append(self._get_inverse_tag(rec_num[0], rec_num[1]))
                        self.circuits[error_prob_num].append(operation[0], [stim.target_rec(i) for i in tmp], operation[2])
        return self.circuits
    
    def output_svg(self, option = "timeline", non_error = False):
        if option == "timeline":
            with open('timeline.svg', 'w') as f:
                if non_error:
                    print(self.circuits[0].without_noise().diagram('timeline-svg'), file=f)
                else:
                    print(self.circuits[0].diagram('timeline-svg'), file=f)
                    
        if option == "timeslice":
            with open('timeslice.svg', 'w') as f:
                if non_error:
                    print(self.circuits[0].without_noise().diagram('timeslice-svg'), file=f)
                else:
                    print(self.circuits[0].diagram('timeslice-svg'), file=f)
    
    def output_circuit_text(self, filename: str):
        for error_prob_num in range(self.error_probabilities_num):
            with open(f'{filename}_{self.error_probabilities[error_prob_num]}.stim', 'w') as f:
                print(self.circuits[error_prob_num], file=f)

    def print_tasks(self):
        print(self.tasks)
        
    def postselct_numbers(self):
        # print(self.postselect)
        return self.postselect
    
    def list_detector(self):
        return self.detector_list
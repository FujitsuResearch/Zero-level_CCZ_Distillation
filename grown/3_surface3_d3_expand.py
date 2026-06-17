from stim_builder import Stim_builder
import numpy as np
import stim
import pymatching
from surface_func import *
error_rate = [1e-3]
distance = 3
distance_expand = 9
circuit_builder = Stim_builder((22, 23), error_rate)

offset = [6, 8] # x, y
offset1 = [5.5, 12.5]
offset2 = [11, 10]
offset3 = [6, 6]
offset4 = [-0.5, 12.5]
offset6 = [0, 0]

q = [(3 + offset[0], 3 + offset[1]), (3.5 + offset[0], 3.5 + offset[1]), (2.5 + offset[0], 3.5 + offset[1]), (3 + offset[0], 4 + offset[1]), (3.5 + offset[0], 2.5 + offset[1]), (4 + offset[0], 3 + offset[1]), (4 + offset[0], 2 + offset[1]), (4.5 + offset[0], 2.5 + offset[1])]

# initialization (x, z)
rotation = ([(-0.5, -0.5), (0.5, -0.5), (-0.5, 0.5), (0.5, 0.5)], [(-0.5, -0.5), (-0.5, 0.5), (0.5, -0.5), (0.5, 0.5)])
rotation2 = ([(0.5, -0.5), (-0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)], [(0.5, -0.5), (0.5, 0.5), (-0.5, -0.5), (-0.5, 0.5)])

surface_data = []
for height in range(distance):
    for width in range(distance):
        surface_data.append((1 + width + offset1[0], 1 + height + offset1[1]))
        surface_data.append((1 + width + offset2[0], 1 + height + offset2[1]))
        surface_data.append((1 + width + offset3[0], 1 + height + offset3[1]))


#1
circuit_builder.rx(q[6])
circuit_builder.rx(q[4])
circuit_builder.rz(q[0])
circuit_builder.rz(q[2])
circuit_builder.rz(q[7])
circuit_builder.rz(q[5])
circuit_builder.rx(q[1])
circuit_builder.rx(q[3])
circuit_builder.tick()

#2
circuit_builder.cnot(q[6], q[7])
circuit_builder.cnot(q[4], q[0])
circuit_builder.cnot(q[1], q[5])
circuit_builder.cnot(q[3], q[2])
circuit_builder.tick()

#3
circuit_builder.cnot(q[6], q[4])
circuit_builder.cnot(q[5], q[7])
circuit_builder.cnot(q[2], q[0])
circuit_builder.cnot(q[1], q[3])
circuit_builder.tick()

#4
circuit_builder.cnot(q[4], q[5])
circuit_builder.cnot(q[0], q[1])
circuit_builder.rx((2.5 + offset[0], 2.5 + offset[1]))
circuit_builder.rx((4 + offset[0], 4 + offset[1]))
circuit_builder.rx((2 + offset[0], 4 + offset[1]))
circuit_builder.rx((2.5 + offset[0], 4.5 + offset[1]))
circuit_builder.rx((3 + offset[0], 2 + offset[1]))
circuit_builder.rx((4.5 + offset[0], 3.5 + offset[1]))
circuit_builder.rx((4.5 + offset[0], 1.5 + offset[1]))
circuit_builder.rx((5 + offset[0], 3 + offset[1]))
circuit_builder.tick()

#5
circuit_builder.cnot((2.5 + offset[0], 2.5 + offset[1]), q[0])
circuit_builder.cnot((4 + offset[0], 4 + offset[1]), q[1])
circuit_builder.cnot((2 + offset[0], 4 + offset[1]), q[2])
circuit_builder.cnot((2.5 + offset[0], 4.5 + offset[1]), q[3])
circuit_builder.cnot((3 + offset[0], 2 + offset[1]), q[4])
circuit_builder.cnot((4.5 + offset[0], 3.5 + offset[1]), q[5])
circuit_builder.cnot((4.5 + offset[0], 1.5 + offset[1]), q[6])
circuit_builder.cnot((5 + offset[0], 3 + offset[1]), q[7])
circuit_builder.tick()

#6
circuit_builder.cnot(q[4], q[5])
circuit_builder.cnot(q[0], q[1])
circuit_builder.tick()

#7
circuit_builder.cnot(q[6], q[4])
circuit_builder.cnot(q[5], q[7])
circuit_builder.cnot(q[2], q[0])
circuit_builder.cnot(q[1], q[3])
circuit_builder.tick()

#8
circuit_builder.cnot(q[6], q[7])
circuit_builder.cnot(q[4], q[0])
circuit_builder.cnot(q[1], q[5])
circuit_builder.cnot(q[3], q[2])
circuit_builder.tick()

#9
circuit_builder.mrx(q[6])
circuit_builder.detector([-1], True)
circuit_builder.mrx(q[4])
circuit_builder.detector([-1], True)
circuit_builder.mrx(q[1])
circuit_builder.detector([-1], True)
circuit_builder.mrx(q[3])
circuit_builder.detector([-1], True)
circuit_builder.tick()

#10
circuit_builder.cnot(q[6], q[7])
circuit_builder.cnot(q[4], q[0])
circuit_builder.cnot(q[1], q[5])
circuit_builder.cnot(q[3], q[2])

circuit_builder.rz((1.5 + offset[0], 4.5 + offset[1]))
circuit_builder.rx((2 + offset[0], 5 + offset[1]))
circuit_builder.rz((5 + offset[0], 4 + offset[1]))
circuit_builder.rx((5.5 + offset[0], 3.5 + offset[1]))
circuit_builder.rz((2 + offset[0], 2 + offset[1]))
circuit_builder.rx((2.5 + offset[0], 1.5 + offset[1]))

surface_data_initialization_x(circuit_builder, distance, offset1)
surface_ancilla_initialization_x(circuit_builder, distance, offset1)
surface_data_initialization_x_rot90(circuit_builder, distance, offset2)
surface_ancilla_initialization_x_rot90(circuit_builder, distance, offset2)
surface_data_initialization_x_mirror_ud(circuit_builder, distance, offset3)
surface_ancilla_initialization_x_mirror_ud(circuit_builder, distance, offset3)

surface_data_initialization_expand(circuit_builder, distance_expand, offset4)
surface_ancilla_initialization_expand(circuit_builder, distance_expand, offset4)
surface_data_initialization_expand_rot90(circuit_builder, distance_expand, offset2)
surface_ancilla_initialization_expand_rot90(circuit_builder, distance_expand, offset2)
surface_data_initialization_expand_mirror_ud(circuit_builder, distance_expand, offset6)
surface_ancilla_initialization_expand_mirror_ud(circuit_builder, distance_expand, offset6)

circuit_builder.tick()

#11
circuit_builder.cnot(q[6], q[4])
circuit_builder.cnot(q[5], q[7])
circuit_builder.cnot(q[2], q[0])
circuit_builder.cnot(q[1], q[3])

circuit_builder.cnot((2 + offset[0], 5 + offset[1]), (1.5 + offset[0], 4.5 + offset[1]))
circuit_builder.cnot((5.5 + offset[0], 3.5 + offset[1]), (5 + offset[0], 4 + offset[1]))
circuit_builder.cnot((2.5 + offset[0], 1.5 + offset[1]), (2 + offset[0], 2 + offset[1]))

circuit_builder.rx((1 + offset[0], 5 + offset[1]))
circuit_builder.rx((5.5 + offset[0], 4.5 + offset[1]))
circuit_builder.rx((1.5 + offset[0], 1.5 + offset[1]))

tick = 0
surface_cnot(circuit_builder, distance_expand, offset4, rotation, tick)
surface_cnot_boundary(circuit_builder, distance_expand, offset4, rotation, tick)
surface_cnot_rot90(circuit_builder, distance_expand, offset2, rotation, tick)
surface_cnot_boundary_rot90(circuit_builder, distance_expand, offset2, rotation, tick)
surface_cnot_mirror_ud(circuit_builder, distance_expand, offset6, rotation, tick)
surface_cnot_boundary_mirror_ud(circuit_builder, distance_expand, offset6, rotation, tick)
circuit_builder.tick()

#12
circuit_builder.cnot(q[4], q[5])
circuit_builder.cnot(q[0], q[1])
circuit_builder.cnot(q[2], (2 + offset[0], 4 + offset[1]))
circuit_builder.cnot(q[3], (2.5 + offset[0], 4.5 + offset[1]))
circuit_builder.cnot(q[6], (4.5 + offset[0], 1.5 + offset[1]))
circuit_builder.cnot(q[7], (5 + offset[0], 3 + offset[1]))

circuit_builder.cnot((1.5 + offset[0], 5.5 + offset[1]), (2 + offset[0], 5 + offset[1]))
circuit_builder.cnot((6 + offset[0], 4 + offset[1]), (5.5 + offset[0], 3.5 + offset[1]))
circuit_builder.cnot((2 + offset[0], 1 + offset[1]), (2.5 + offset[0], 1.5 + offset[1]))

circuit_builder.cnot((1 + offset[0], 5 + offset[1]), (0.5 + offset[0], 5.5 + offset[1]))
circuit_builder.cnot((5.5 + offset[0], 4.5 + offset[1]), (6 + offset[0], 5 + offset[1]))
circuit_builder.cnot((1.5 + offset[0], 1.5 + offset[1]), (1 + offset[0], 1 + offset[1]))

tick = 1
surface_cnot(circuit_builder, distance_expand, offset4, rotation, tick)
surface_cnot_boundary(circuit_builder, distance_expand, offset4, rotation, tick)
surface_cnot_rot90(circuit_builder, distance_expand, offset2, rotation, tick)
surface_cnot_boundary_rot90(circuit_builder, distance_expand, offset2, rotation, tick)
surface_cnot_mirror_ud(circuit_builder, distance_expand, offset6, rotation, tick)
surface_cnot_boundary_mirror_ud(circuit_builder, distance_expand, offset6, rotation, tick)
circuit_builder.tick()

#13
circuit_builder.cnot(q[0], (2.5 + offset[0], 2.5 + offset[1]))
circuit_builder.cnot((4 + offset[0], 4 + offset[1]), q[1])
circuit_builder.cnot(q[4], (3 + offset[0], 2 + offset[1]))
circuit_builder.cnot(q[5], (4.5 + offset[0], 3.5 + offset[1]))

circuit_builder.mx(q[2])
circuit_builder.detector([-1], True)
circuit_builder.mx(q[3])
circuit_builder.detector([-1], True)
circuit_builder.mx(q[6])
circuit_builder.detector([-1], True)
circuit_builder.mx(q[7])
circuit_builder.detector([-1], True)

circuit_builder.mrz((0.5 + offset[0], 5.5 + offset[1]))
circuit_builder.classical_cnot((1 + offset[0], 5 + offset[1]))
circuit_builder.mrz((6 + offset[0], 5 + offset[1]))
circuit_builder.classical_cnot((5.5 + offset[0], 4.5 + offset[1]))
circuit_builder.mrz((1 + offset[0], 1 + offset[1]))
circuit_builder.classical_cnot((1.5 + offset[0], 1.5 + offset[1]))

circuit_builder.cnot((1 + offset[0], 5 + offset[1]), (1.5 + offset[0], 4.5 + offset[1]))
circuit_builder.cnot((2.5 + offset[0], 5.5 + offset[1]), (2 + offset[0], 5 + offset[1]))
circuit_builder.cnot((5.5 + offset[0], 4.5 + offset[1]), (5 + offset[0], 4 + offset[1]))
circuit_builder.cnot((6 + offset[0], 3 + offset[1]), (5.5 + offset[0], 3.5 + offset[1]))
circuit_builder.cnot((1.5 + offset[0], 1.5 + offset[1]), (2 + offset[0], 2 + offset[1]))
circuit_builder.cnot((3 + offset[0], 1 + offset[1]), (2.5 + offset[0], 1.5 + offset[1]))

tick = 2
surface_cnot(circuit_builder, distance_expand, offset4, rotation, tick)
surface_cnot_boundary(circuit_builder, distance_expand, offset4, rotation, tick)
surface_cnot_rot90(circuit_builder, distance_expand, offset2, rotation, tick)
surface_cnot_boundary_rot90(circuit_builder, distance_expand, offset2, rotation, tick)
surface_cnot_mirror_ud(circuit_builder, distance_expand, offset6, rotation, tick)
surface_cnot_boundary_mirror_ud(circuit_builder, distance_expand, offset6, rotation, tick)
circuit_builder.tick()

#14
circuit_builder.mrx(q[0])
circuit_builder.detector([-1], True)
circuit_builder.mrx((4 + offset[0], 4 + offset[1]))
circuit_builder.detector([-1], True)
circuit_builder.mrx(q[4])
circuit_builder.detector([-1], True)
circuit_builder.mrx(q[5])
circuit_builder.detector([-1], True)

circuit_builder.cnot((2 + offset[0], 4 + offset[1]), (1.5 + offset[0], 4.5 + offset[1]))
circuit_builder.cnot((2.5 + offset[0], 4.5 + offset[1]), (2 + offset[0], 5 + offset[1]))
circuit_builder.cnot((5 + offset[0], 3 + offset[1]), (5.5 + offset[0], 3.5 + offset[1]))
circuit_builder.cnot((4.5 + offset[0], 3.5 + offset[1]), (5 + offset[0], 4 + offset[1]))
circuit_builder.cnot((3 + offset[0], 2 + offset[1]), (2.5 + offset[0], 1.5 + offset[1]))
circuit_builder.cnot((2.5 + offset[0], 2.5 + offset[1]), (2 + offset[0], 2 + offset[1]))

tick = 3
surface_cnot(circuit_builder, distance_expand, offset4, rotation, tick)
surface_cnot_boundary(circuit_builder, distance_expand, offset4, rotation, tick)
surface_cnot_rot90(circuit_builder, distance_expand, offset2, rotation, tick)
surface_cnot_boundary_rot90(circuit_builder, distance_expand, offset2, rotation, tick)
surface_cnot_mirror_ud(circuit_builder, distance_expand, offset6, rotation, tick)
surface_cnot_boundary_mirror_ud(circuit_builder, distance_expand, offset6, rotation, tick)
circuit_builder.tick()

# 15
circuit_builder.rx((3 + offset[0], 3 + offset[1]))
circuit_builder.rz((3.5 + offset[0], 2.5 + offset[1]))

circuit_builder.cnot((2 + offset[0], 5 + offset[1]), (1.5 + offset[0], 4.5 + offset[1]))
circuit_builder.cnot((5.5 + offset[0], 3.5 + offset[1]), (5 + offset[0], 4 + offset[1]))
circuit_builder.cnot((2.5 + offset[0], 1.5 + offset[1]), (2 + offset[0], 2 + offset[1]))

circuit_builder.rz((0.5 + offset[0], 5.5 + offset[1]))
circuit_builder.rz((6 + offset[0], 5 + offset[1]))
circuit_builder.rz((1 + offset[0], 1 + offset[1]))

tag = 1000
tag = surface_measurement_first_expand(circuit_builder, distance_expand, offset4, tag)
tag = 2000
tag = surface_measurement_first_expand_rot90(circuit_builder, distance_expand, offset2, tag)
tag = 3000
tag = surface_measurement_first_expand_mirror_ud(circuit_builder, distance_expand, offset6, tag)
circuit_builder.tick()

#16
circuit_builder.rz(q[2])
circuit_builder.rz(q[3])
circuit_builder.rz(q[5])
circuit_builder.rz(q[6])
circuit_builder.rz(q[7])
circuit_builder.cnot((3 + offset[0], 3 + offset[1]), (3.5 + offset[0], 2.5 + offset[1]))

circuit_builder.mrx((2 + offset[0], 5 + offset[1]))
circuit_builder.detector([-1], True)
circuit_builder.mrz((1.5 + offset[0], 4.5 + offset[1]), "zz_1")
circuit_builder.mrx((5.5 + offset[0], 3.5 + offset[1]))
circuit_builder.detector([-1], True)
circuit_builder.mrz((5 + offset[0], 4 + offset[1]), "zz_2")
circuit_builder.mrx((2.5 + offset[0], 1.5 + offset[1]))
circuit_builder.detector([-1], True)
circuit_builder.mrz((2 + offset[0], 2 + offset[1]), "zz_3")

# circuit_builder.ideal_start()
tick = 0
surface_cnot_2(circuit_builder, distance_expand, offset4, rotation2, tick)
surface_cnot_boundary(circuit_builder, distance_expand, offset4, rotation2, tick)
surface_cnot_2_rot90(circuit_builder, distance_expand, offset2, rotation2, tick)
surface_cnot_boundary_rot90(circuit_builder, distance_expand, offset2, rotation2, tick)
surface_cnot_2_mirror_ud(circuit_builder, distance_expand, offset6, rotation2, tick)
surface_cnot_boundary_mirror_ud(circuit_builder, distance_expand, offset6, rotation2, tick)
# circuit_builder.ideal_end()
circuit_builder.tick()

# 17
circuit_builder.cnot((3.5 + offset[0], 2.5 + offset[1]), (4 + offset[0], 2 + offset[1]))
circuit_builder.cnot((3 + offset[0], 3 + offset[1]), (2.5 + offset[0], 3.5 + offset[1]))
circuit_builder.cnot((5 + offset[0], 3 + offset[1]), (4.5 + offset[0], 2.5 + offset[1]))
circuit_builder.cnot((4.5 + offset[0], 3.5 + offset[1]), (4 + offset[0], 3 + offset[1]))
circuit_builder.cnot((2.5 + offset[0], 4.5 + offset[1]), (3 + offset[0], 4 + offset[1]))

circuit_builder.cnot((2 + offset[0], 5 + offset[1]), (1.5 + offset[0], 4.5 + offset[1]))
circuit_builder.cnot((5.5 + offset[0], 3.5 + offset[1]), (5 + offset[0], 4 + offset[1]))
circuit_builder.cnot((2.5 + offset[0], 1.5 + offset[1]), (2 + offset[0], 2 + offset[1]))

circuit_builder.cnot((1 + offset[0], 5 + offset[1]), (0.5 + offset[0], 5.5 + offset[1]))
circuit_builder.cnot((5.5 + offset[0], 4.5 + offset[1]), (6 + offset[0], 5 + offset[1]))
circuit_builder.cnot((1.5 + offset[0], 1.5 + offset[1]), (1 + offset[0], 1 + offset[1]))

# circuit_builder.ideal_start()
tick = 1
surface_cnot_2(circuit_builder, distance_expand, offset4, rotation2, tick)
surface_cnot_boundary(circuit_builder, distance_expand, offset4, rotation2, tick)
surface_cnot_2_rot90(circuit_builder, distance_expand, offset2, rotation2, tick)
surface_cnot_boundary_rot90(circuit_builder, distance_expand, offset2, rotation2, tick)
surface_cnot_2_mirror_ud(circuit_builder, distance_expand, offset6, rotation2, tick)
surface_cnot_boundary_mirror_ud(circuit_builder, distance_expand, offset6, rotation2, tick)
# circuit_builder.ideal_end()
circuit_builder.tick()

# 18
circuit_builder.cnot((4 + offset[0], 2 + offset[1]), (4.5 + offset[0], 2.5 + offset[1]))
circuit_builder.cnot((3.5 + offset[0], 2.5 + offset[1]), (4 + offset[0], 3 + offset[1]))
circuit_builder.cnot((3 + offset[0], 3 + offset[1]), (3.5 + offset[0], 3.5 + offset[1]))
circuit_builder.cnot((2.5 + offset[0], 3.5 + offset[1]), (3 + offset[0], 4 + offset[1]))

circuit_builder.cnot((2 + offset[0], 4 + offset[1]), (1.5 + offset[0], 4.5 + offset[1]))
circuit_builder.cnot((2.5 + offset[0], 4.5 + offset[1]), (2 + offset[0], 5 + offset[1]))
circuit_builder.cnot((5 + offset[0], 3 + offset[1]), (5.5 + offset[0], 3.5 + offset[1]))
circuit_builder.cnot((4.5 + offset[0], 3.5 + offset[1]), (5 + offset[0], 4 + offset[1]))
circuit_builder.cnot((3 + offset[0], 2 + offset[1]), (2.5 + offset[0], 1.5 + offset[1]))
circuit_builder.cnot((2.5 + offset[0], 2.5 + offset[1]), (2 + offset[0], 2 + offset[1]))

# circuit_builder.ideal_start()
tick = 2
surface_cnot_2(circuit_builder, distance_expand, offset4, rotation2, tick)
surface_cnot_boundary(circuit_builder, distance_expand, offset4, rotation2, tick)
surface_cnot_2_rot90(circuit_builder, distance_expand, offset2, rotation2, tick)
surface_cnot_boundary_rot90(circuit_builder, distance_expand, offset2, rotation2, tick)
surface_cnot_2_mirror_ud(circuit_builder, distance_expand, offset6, rotation2, tick)
surface_cnot_boundary_mirror_ud(circuit_builder, distance_expand, offset6, rotation2, tick)
# circuit_builder.ideal_end()
circuit_builder.tick()

# 19
circuit_builder.mx((5 + offset[0], 3 + offset[1]))
circuit_builder.classical_cz((4.5 + offset[0], 2.5 + offset[1]))
circuit_builder.classical_cz((4 + offset[0], 2 + offset[1]))
circuit_builder.mrx((4.5 + offset[0], 3.5 + offset[1]))
circuit_builder.classical_cz((4 + offset[0], 3 + offset[1]))
circuit_builder.classical_cz((3.5 + offset[0], 2.5 + offset[1]))
circuit_builder.mx((2.5 + offset[0], 4.5 + offset[1]))
circuit_builder.classical_cz((2.5 + offset[0], 3.5 + offset[1]))
circuit_builder.classical_cz((3 + offset[0], 4 + offset[1]))
circuit_builder.rz((4 + offset[0], 4 + offset[1]))
circuit_builder.cnot((2.5 + offset[0], 3.5 + offset[1]), (2 + offset[0], 4 + offset[1]))
circuit_builder.cnot((4 + offset[0], 2 + offset[1]), (4.5 + offset[0], 1.5 + offset[1]))
circuit_builder.cnot((3.5 + offset[0], 2.5 + offset[1]), (3 + offset[0], 2 + offset[1]))
circuit_builder.cnot((3 + offset[0], 3 + offset[1]), (2.5 + offset[0], 2.5 + offset[1]))

circuit_builder.cnot((1 + offset[0], 5 + offset[1]), (1.5 + offset[0], 4.5 + offset[1]))
circuit_builder.cnot((1.5 + offset[0], 5.5 + offset[1]), (2 + offset[0], 5 + offset[1]))
circuit_builder.cnot((5.5 + offset[0], 4.5 + offset[1]), (5 + offset[0], 4 + offset[1]))
circuit_builder.cnot((6 + offset[0], 4 + offset[1]), (5.5 + offset[0], 3.5 + offset[1]))
circuit_builder.cnot((1.5 + offset[0], 1.5 + offset[1]), (2 + offset[0], 2 + offset[1]))
circuit_builder.cnot((2 + offset[0], 1 + offset[1]), (2.5 + offset[0], 1.5 + offset[1]))

# circuit_builder.ideal_start()
tick = 3
surface_cnot_2(circuit_builder, distance_expand, offset4, rotation2, tick)
surface_cnot_boundary(circuit_builder, distance_expand, offset4, rotation2, tick)
surface_cnot_2_rot90(circuit_builder, distance_expand, offset2, rotation2, tick)
surface_cnot_boundary_rot90(circuit_builder, distance_expand, offset2, rotation2, tick)
surface_cnot_2_mirror_ud(circuit_builder, distance_expand, offset6, rotation2, tick)
surface_cnot_boundary_mirror_ud(circuit_builder, distance_expand, offset6, rotation2, tick)
# circuit_builder.ideal_end()
circuit_builder.tick()

# 20
circuit_builder.cnot((4.5 + offset[0], 2.5 + offset[1]), (4 + offset[0], 2 + offset[1]))
circuit_builder.cnot((4 + offset[0], 3 + offset[1]), (3.5 + offset[0], 2.5 + offset[1]))
circuit_builder.cnot((3.5 + offset[0], 3.5 + offset[1]), (3 + offset[0], 3 + offset[1]))
circuit_builder.cnot((3 + offset[0], 4 + offset[1]), (2.5 + offset[0], 3.5 + offset[1]))
circuit_builder.rz((5 + offset[0], 3 + offset[1]))
circuit_builder.rz((3.5 + offset[0], 4.5 + offset[1]))
circuit_builder.cnot((4.5 + offset[0], 3.5 + offset[1]), (4 + offset[0], 4 + offset[1]))

circuit_builder.cnot((2.5 + offset[0], 5.5 + offset[1]), (2 + offset[0], 5 + offset[1]))
circuit_builder.cnot((6 + offset[0], 3 + offset[1]), (5.5 + offset[0], 3.5 + offset[1]))
circuit_builder.cnot((3 + offset[0], 1 + offset[1]), (2.5 + offset[0], 1.5 + offset[1]))

circuit_builder.mx((1 + offset[0], 5 + offset[1]))
circuit_builder.classical_cz((0.5 + offset[0], 5.5 + offset[1]))
circuit_builder.classical_cz((0 + offset[0], 6 + offset[1]))
circuit_builder.mx((5.5 + offset[0], 4.5 + offset[1]))
circuit_builder.classical_cz((6 + offset[0], 5 + offset[1]))
circuit_builder.classical_cz((6.5 + offset[0], 5.5 + offset[1]))
circuit_builder.mx((1.5 + offset[0], 1.5 + offset[1]))
circuit_builder.classical_cz((1 + offset[0], 1 + offset[1]))
circuit_builder.classical_cz((0.5 + offset[0], 0.5 + offset[1]))

tag = 1000
tag = surface_measurement(circuit_builder, distance_expand, offset4, tag)
tag = 2000
tag = surface_measurement_rot90(circuit_builder, distance_expand, offset2, tag)
tag = 3000
tag = surface_measurement_mirror_ud(circuit_builder, distance_expand, offset6, tag)
circuit_builder.tick()

# 21
circuit_builder.cnot((4.5 + offset[0], 1.5 + offset[1]), (4 + offset[0], 2 + offset[1]))
circuit_builder.cnot((3 + offset[0], 2 + offset[1]), (3.5 + offset[0], 2.5 + offset[1]))
circuit_builder.cnot((2.5 + offset[0], 2.5 + offset[1]), (3 + offset[0], 3 + offset[1]))
circuit_builder.cnot((2 + offset[0], 4 + offset[1]), (2.5 + offset[0], 3.5 + offset[1]))
circuit_builder.cnot((4.5 + offset[0], 2.5 + offset[1]), (5 + offset[0], 3 + offset[1]))
circuit_builder.cnot((4 + offset[0], 3 + offset[1]), (4.5 + offset[0], 3.5 + offset[1]))
circuit_builder.cnot((3.5 + offset[0], 3.5 + offset[1]), (4 + offset[0], 4 + offset[1]))
circuit_builder.cnot((3 + offset[0], 4 + offset[1]), (3.5 + offset[0], 4.5 + offset[1]))

circuit_builder.cnot((2 + offset[0], 5 + offset[1]), (1.5 + offset[0], 4.5 + offset[1]))
circuit_builder.cnot((5.5 + offset[0], 3.5 + offset[1]), (5 + offset[0], 4 + offset[1]))
circuit_builder.cnot((2.5 + offset[0], 1.5 + offset[1]), (2 + offset[0], 2 + offset[1]))

surface_data = []
for height in range(distance_expand):
    for width in range(distance_expand):
        surface_data.append((1 + width + offset4[0], 1 + height + offset4[1]))
        surface_data.append((1 + width + offset2[0], 1 + height + offset2[1]))
        surface_data.append((1 + width + offset6[0], 1 + height + offset6[1]))
circuit_builder.ideal(surface_data)
circuit_builder.tick()

# 22
circuit_builder.mx((4.5 + offset[0], 2.5 + offset[1]))
circuit_builder.classical_cz((5 + offset[0], 3 + offset[1]))
circuit_builder.mx((3 + offset[0], 4 + offset[1]))
circuit_builder.classical_cz((3.5 + offset[0], 4.5 + offset[1]))

circuit_builder.cnot((3.5 + offset[0], 2.5 + offset[1]), (4 + offset[0], 2 + offset[1]))
circuit_builder.cnot((3 + offset[0], 3 + offset[1]), (2.5 + offset[0], 3.5 + offset[1]))
circuit_builder.cnot((5 + offset[0], 3 + offset[1]), (4.5 + offset[0], 3.5 + offset[1]))
circuit_builder.cnot((3.5 + offset[0], 4.5 + offset[1]), (4 + offset[0], 4 + offset[1]))

circuit_builder.mrx((2 + offset[0], 5 + offset[1]))
circuit_builder.detector([-1], True)
circuit_builder.mrz((1.5 + offset[0], 4.5 + offset[1]), "zz_1")
circuit_builder.detector([-1, ("zz_1", -2)], True)
circuit_builder.mrx((5.5 + offset[0], 3.5 + offset[1]))
circuit_builder.detector([-1], True)
circuit_builder.mrz((5 + offset[0], 4 + offset[1]), "zz_2")
circuit_builder.detector([-1, ("zz_2", -2)], True)
circuit_builder.mrx((2.5 + offset[0], 1.5 + offset[1]))
circuit_builder.detector([-1], True)
circuit_builder.mrz((2 + offset[0], 2 + offset[1]), "zz_3")
circuit_builder.detector([-1, ("zz_3", -2)], True)

data_832 = [(3 + offset[0], 2 + offset[1]), (3.5 + offset[0], 3.5 + offset[1]), (2 + offset[0], 4 + offset[1]), (2.5 + offset[0], 2.5 + offset[1]), (4 + offset[0], 3 + offset[1]), (4.5 + offset[0], 1.5 + offset[1])]
circuit_builder.ideal(data_832)
circuit_builder.ideal(surface_data)
circuit_builder.tick()

# 23
circuit_builder.cnot((3 + offset[0], 3 + offset[1]), (3.5 + offset[0], 2.5 + offset[1]))
circuit_builder.cnot((4 + offset[0], 4 + offset[1]), (4.5 + offset[0], 3.5 + offset[1]))

circuit_builder.mz((2.5 + offset[0], 3.5 + offset[1]))
circuit_builder.detector([-1], True)
circuit_builder.mz((4 + offset[0], 2 + offset[1]))
circuit_builder.detector([-1], True)

data_832 = [(3 + offset[0], 2 + offset[1]), (3.5 + offset[0], 3.5 + offset[1]), (2 + offset[0], 4 + offset[1]), (3.5 + offset[0], 4.5 + offset[1]), (2.5 + offset[0], 2.5 + offset[1]), (4 + offset[0], 3 + offset[1]), (4.5 + offset[0], 1.5 + offset[1]), (5 + offset[0], 3 + offset[1])]
circuit_builder.ideal(data_832)
circuit_builder.ideal(surface_data)
circuit_builder.tick()

# 24
circuit_builder.mx((3 + offset[0], 3 + offset[1]))
circuit_builder.detector([-1], True)
circuit_builder.mz((3.5 + offset[0], 2.5 + offset[1]))
circuit_builder.detector([-1], True)
circuit_builder.mx((4 + offset[0], 4 + offset[1]))
circuit_builder.detector([-1], True)
circuit_builder.mz((4.5 + offset[0], 3.5 + offset[1]))
circuit_builder.detector([-1], True)

circuit_builder.mx((2.5 + offset[0], 2.5 + offset[1]), "data")
circuit_builder.mx((3.5 + offset[0], 3.5 + offset[1]), "data")
circuit_builder.mx((2 + offset[0], 4 + offset[1]), "data")
circuit_builder.mx((3.5 + offset[0], 4.5 + offset[1]), "data")
circuit_builder.mx((3 + offset[0], 2 + offset[1]), "data")
circuit_builder.mx((4 + offset[0], 3 + offset[1]), "data")
circuit_builder.mx((4.5 + offset[0], 1.5 + offset[1]), "data")
circuit_builder.mx((5 + offset[0], 3 + offset[1]), "data")
circuit_builder.detector([-1, -2, -3, -4, -5, -6, -7, -8], True)

surface_ancilla_initialization_expand_2(circuit_builder, distance_expand, offset4)
surface_ancilla_initialization_expand_2_rot90(circuit_builder, distance_expand, offset2)
surface_ancilla_initialization_expand_2_mirror_ud(circuit_builder, distance_expand, offset6)
circuit_builder.tick()

for j in range(1):
    for i in range(4):
        surface_cnot_2(circuit_builder, distance_expand, offset4, rotation2, i)
        surface_cnot_boundary_2(circuit_builder, distance_expand, offset4, rotation2, i)
        surface_cnot_2_rot90(circuit_builder, distance_expand, offset2, rotation2, i)
        surface_cnot_boundary_2_rot90(circuit_builder, distance_expand, offset2, rotation2, i)
        surface_cnot_2_mirror_ud(circuit_builder, distance_expand, offset6, rotation2, i)
        surface_cnot_boundary_2_mirror_ud(circuit_builder, distance_expand, offset6, rotation2, i)
        circuit_builder.tick()

    tag = 1000
    tag = surface_measurement_2(circuit_builder, distance_expand, offset4, tag)
    tag = 2000
    tag = surface_measurement_2_rot90(circuit_builder, distance_expand, offset2, tag)
    tag = 3000
    tag = surface_measurement_2_mirror_ud(circuit_builder, distance_expand, offset6, tag)
    circuit_builder.tick()

circuit_builder.ideal_start()

surface_ancilla_initialization_expand_2(circuit_builder, distance_expand, offset4)
surface_ancilla_initialization_expand_2_rot90(circuit_builder, distance_expand, offset2)
surface_ancilla_initialization_expand_2_mirror_ud(circuit_builder, distance_expand, offset6)
circuit_builder.tick()

for i in range(4):
    surface_cnot_2(circuit_builder, distance_expand, offset4, rotation2, i)
    surface_cnot_boundary_2(circuit_builder, distance_expand, offset4, rotation2, i)
    surface_cnot_2_rot90(circuit_builder, distance_expand, offset2, rotation2, i)
    surface_cnot_boundary_2_rot90(circuit_builder, distance_expand, offset2, rotation2, i)
    surface_cnot_2_mirror_ud(circuit_builder, distance_expand, offset6, rotation2, i)
    surface_cnot_boundary_2_mirror_ud(circuit_builder, distance_expand, offset6, rotation2, i)
    circuit_builder.tick()

tag = 1000
tag = surface_measurement_3(circuit_builder, distance_expand, offset4, tag)
tag = 2000
tag = surface_measurement_3_rot90(circuit_builder, distance_expand, offset2, tag)
tag = 3000
tag = surface_measurement_3_mirror_ud(circuit_builder, distance_expand, offset6, tag)
circuit_builder.tick()

for height in range(distance_expand):
    circuit_builder.mx((1 + offset1[0], 1 + height + offset1[1]))
obs = [("data", 0), ("data", 2), ("data", 4), ("data", 6)]
obs += [-1 - l for l in range(distance_expand)]
circuit_builder.observable(obs)

for width in range(distance_expand):
    circuit_builder.mx((1 + width + offset2[0], 1 + offset2[1]))
obs_2 = [("data", 0), ("data", 1), ("data", 4), ("data", 5)]
obs_2 += [-1 - l for l in range(distance_expand)]
circuit_builder.observable(obs_2)

for height in range(distance_expand):
    circuit_builder.mx((distance_expand + offset6[0], 1 + height + offset6[1]))
obs_3 = [("data", 0), ("data", 1), ("data", 2), ("data", 3)]
obs_3 += [-1 - l for l in range(distance_expand)]
circuit_builder.observable(obs_3)


circuit = circuit_builder.build()
circuit_builder.output_svg("timeline")
circuit_builder.output_svg("timeslice", True)
circuit_builder.output_circuit_text("832_text")

with open(f'832_text_{error_rate[0]}.stim', 'r') as crumble:
    circuit = stim.Circuit(crumble.read())
# with open(f'832_text_{error_rate[0]}.stim', 'r') as crumble:
#     circuit_detector = stim.Circuit(crumble.read())


shots = 10 ** 6
# shots = 10
dem = circuit.detector_error_model(decompose_errors=True)
matcher = pymatching.Matching.from_detector_error_model(dem)
sampler = circuit.compile_detector_sampler()
syndrome, actual_observables = sampler.sample(shots, separate_observables=True)
num_errors = 0
non_error = 0
detect = 0

postselect = circuit_builder.postselct_numbers()
ps_cnt = len(postselect)
dete = circuit_builder.list_detector()

# # for i in range(shots):
# #     if any(syndrome[i]):
# #         detect += 1
# #     else:
# #         if any(actual_observables[i]):
# #             num_errors += 1
# #         else:
# #             non_error += 1


for i in range(shots):
    detec = False
    for ps_num in range(ps_cnt):
        if postselect[ps_num] and syndrome[i][ps_num]:
            detect += 1
            detec = True
            break
    if detec == True:
        continue
    
    prediction = matcher.decode(syndrome[i])
    # print(prediction)
    # print(actual_observables)
    if not np.array_equal(actual_observables[i], prediction):
        num_errors += 1
    else:
        non_error += 1
    
# # for i in range(shots):
# #     if any(syndrome[i]):
# #         detect += 1
# #     else:
# #         prediction = matcher.decode(syndrome[i])
# #         if not np.array_equal(actual_observables[i], prediction):
# #             num_errors += 1
# #         else:
# #             non_error += 1

print("logical error", num_errors)
print("detect", detect)
print("success", non_error)
print("error rate", num_errors / (shots - detect))
print("success rate", (shots - detect) / shots)


"""
1e-3, 1e6, 0.00034852566383247535, 0.275446
8e-4, 5e6, 0.0002219381364258208, 0.3568562
6e-4, 5e6, 0.00011960131162771752, 0.4615334
4e-4, 5e6, 5.422499759000011e-05, 0.5975104
2e-4, 1e7, 1.3586052894515038e-05, 0.7728514
1e-4, 1e7, 3.866977783985162e-06, 0.8792396
"""
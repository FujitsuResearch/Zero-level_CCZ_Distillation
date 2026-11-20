"""Gate schedule from the CCZ branch of Fig. 14, in Qulacs qubit order."""


def build_figure14(b):
    # Round 1
    b.reset_z(4)
    b.reset_z(5)
    b.reset_x(6)
    b.reset_x(7)
    b.reset_x(8)
    b.reset_x(9)
    b.reset_z(10)
    b.reset_z(11)

    # Round 2
    b.cx(8, 4)
    b.cx(6, 5)
    b.cx(9, 10)
    b.cx(7, 11)

    # Round 3
    b.cx(4, 5)
    b.cx(7, 6)
    b.cx(9, 8)
    b.cx(10, 11)

    # Round 4
    b.cx(5, 9)
    b.cx(6, 10)
    b.reset_x(0)
    b.reset_x(1)
    b.reset_x(2)
    b.reset_x(3)
    b.reset_x(12)
    b.reset_x(13)
    b.reset_x(14)
    b.reset_x(15)
    b.idle(4, 7, 8, 11)

    # Round 5
    b.cx(0, 4)
    b.cx(1, 5)
    b.cx(2, 6)
    b.cx(3, 7)
    b.cx(12, 8)
    b.cx(13, 9)
    b.cx(14, 10)
    b.cx(15, 11)

    # Round 6
    b.cx(5, 9)
    b.cx(6, 10)
    b.idle(4, 7, 8, 11)
    b.idle(0, 1, 2, 3, 12, 13, 14, 15)

    # Round 7
    b.cx(4, 5)
    b.cx(7, 6)
    b.cx(9, 8)
    b.cx(10, 11)
    b.idle(0, 1, 2, 3, 12, 13, 14, 15)

    # Round 8
    b.cx(8, 4)
    b.cx(6, 5)
    b.cx(9, 10)
    b.cx(7, 11)
    b.idle(0, 1, 2, 3, 12, 13, 14, 15)

    # Round 9
    b.mes_reset_x(6, 0)
    b.mes_reset_x(7, 1)
    b.mes_reset_x(8, 2)
    b.mes_reset_x(9, 3)
    b.idle(4, 5, 10, 11)
    b.idle(0, 1, 2, 3, 12, 13, 14, 15)

    # Round 10
    b.cx(8, 4)
    b.cx(6, 5)
    b.cx(9, 10)
    b.cx(7, 11)
    b.idle(0, 1, 2, 3, 12, 13, 14, 15)

    # Round 11
    b.cx(4, 5)
    b.cx(7, 6)
    b.cx(9, 8)
    b.cx(10, 11)
    b.idle(0, 1, 2, 3, 12, 13, 14, 15)

    # Round 12
    b.cx(5, 9)
    b.cx(6, 10)
    b.cx(4, 0)
    b.cx(7, 3)
    b.cx(8, 12)
    b.cx(11, 15)
    b.idle(1, 2, 13, 14)

    # Round 13
    b.cx(5, 1)
    b.cx(6, 2)
    b.cx(13, 9)
    b.cx(10, 14)
    b.mes_x(4, 4)
    b.mes_x(7, 5)
    b.mes_x(8, 6)
    b.mes_x(11, 7)
    b.idle(0, 3, 12, 15)

    # Round 14
    b.mes_x(5, 8)
    b.mes_x(6, 9)
    b.mes_x(10, 10)
    b.mes_x(13, 11)
    b.idle(0, 1, 2, 12, 14, 15, interface=True)
    b.idle(3, 9)
    b.reject(12)

    # Round 15
    b.reset_x(5)
    b.reset_z(6)
    b.idle(0, 1, 2, 3, 9, 12, 14, 15)

    # Round 16
    b.cx(5, 6)
    b.reset_z(4)
    b.reset_z(7)
    b.reset_z(8)
    b.reset_z(10)
    b.reset_z(11)
    b.t(1)
    b.tdag(9)
    b.tdag(0)
    b.t(12)
    b.tdag(2)
    b.t(14)
    b.t(3)
    b.tdag(15)

    # Round 17
    b.cx(5, 4)
    b.cx(6, 7)
    b.cx(12, 8)
    b.cx(14, 10)
    b.cx(15, 11)
    b.idle(0, 1, 2, 3, 9)

    # Round 18
    b.cx(4, 8)
    b.cx(5, 9)
    b.cx(6, 10)
    b.cx(7, 11)
    b.idle(0, 1, 2, 12, 14, 15, interface=True)
    b.idle(3)

    # Round 19
    b.cx(4, 0)
    b.cx(5, 1)
    b.cx(6, 2)
    b.cx(7, 3)
    b.reset_z(13)
    b.mes_x(12, 0)
    b.mes_reset_x(14, 1)
    b.mes_x(15, 2)
    b.idle(9)
    b.correct(0, ("Z", 4), ("Z", 8), ("X", 12))
    b.correct(1, ("Z", 6), ("Z", 10), ("Z", 14))
    b.correct(2, ("Z", 7), ("Z", 11), ("X", 15))

    # Round 20
    b.cx(8, 4)
    b.cx(9, 5)
    b.cx(10, 6)
    b.cx(11, 7)
    b.cx(14, 13)
    b.reset_z(12)
    b.reset_z(15)
    b.idle(0, 1, 2, 3)

    # Round 21
    b.cx(0, 4)
    b.cx(1, 5)
    b.cx(2, 6)
    b.cx(3, 7)
    b.cx(8, 12)
    b.cx(9, 13)
    b.cx(10, 14)
    b.cx(11, 15)

    # Round 22
    b.cx(5, 4)
    b.cx(6, 7)
    b.cx(12, 13)
    b.cx(15, 14)
    b.mes_x(8, 0)
    b.mes_x(11, 1)
    b.correct(0, ("Z", 12), ("X", 8))
    b.correct(1, ("Z", 15), ("X", 11))

    # Round 23
    b.cx(5, 6)
    b.cx(13, 14)
    b.mes_z(4, 0)
    b.mes_z(7, 1)

    # Round 24
    b.mes_x(5, 2)
    b.mes_z(6, 3)
    b.mes_x(13, 4)
    b.mes_z(14, 5)
    b.swap(0, 1)
    b.swap(1, 9)
    b.swap(9, 2)
    b.swap(3, 12)
    b.swap(4, 9)
    b.swap(5, 10)
    b.swap(6, 12)
    b.swap(7, 15)
    b.reject(6)

    # Ideal stabilizer readout, with the four-bit acceptance rule used in Fig. 14.
    for i in range(7):
        b.ideal_cx(i + 1, i)
    b.h(7)
    b.measure(7, 0)
    b.h(7)
    for i in reversed(range(7)):
        b.ideal_cx(i + 1, i)
    for register, qubits in enumerate(((0, 1, 2, 3), (4, 5, 6, 7),
                                       (0, 1, 4, 5), (0, 2, 4, 6)), start=1):
        pairs = list(zip(qubits, qubits[1:]))
        for control, target in pairs:
            b.ideal_cx(control, target)
        b.measure(qubits[-1], register)
        for control, target in reversed(pairs):
            b.ideal_cx(control, target)
    b.reject(4)

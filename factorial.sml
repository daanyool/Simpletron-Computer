0000	read n
0001	loadI 1
0002	store initOne
0003	loadM n
0004	subM initOne
0005	store deductedN
0006	mulM n
0007	store fact
0008	jz display
0009	loadM deductedN
0010	subM initOne
0011	store deductedN
0012	jz display
0013	mulM fact
0014	store fact
0015	jmp x
0016	write fact
0017	halt 0
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

#include "timing.h"

void write_solution(char const* filename, int Xmax, int Ymax, double **I)
{
    int i, j;
    FILE *fp = fopen(filename, "w+");
    for (i = 0; i < Ymax; ++i)
	{
		for (j = 0; j < Xmax; ++j)
		{
			fprintf(fp, "%g ", I[i][j]);
		}
		fprintf(fp, "\n");
	}
    fclose(fp);
}

void initialise(double ** S, double ** I, double ** R, int Xmax, int Ymax) 
{
	/* 
	Assume epicenter of spread is NY, which has roughly 15% horizontal width and 20% vertical length.
	Assume that NY is hence [0.8, 0.95] horizontally and [0.15, 0.35] vertically.
	*/
	int NYx_low = 0.8 * Xmax;
	int NYx_high = 0.95 * Xmax;
	int NYy_low = 0.15 * Ymax;
	int NYy_high = 0.35 * Ymax;

	for (int i = 0; i < Ymax; ++i) 
	{
		for (int j = 0; j < Xmax; ++j) 
		{
			if ((NYy_low <= i) && (i < NYy_high) && (NYx_low <= j) && (j < NYx_high)) 
			{
				I[i][j] = 0.01;
				S[i][j] = 0.99;
			} 
			else 
			{
				S[i][j] = 1.0;
			}
		}
	}
}

void simulate(int nsweeps, double **S, double **I, double **R, double beta, 
double gamma, double dS, double dI, double dR, int Xmax, int Ymax) 
{
	/* Initialize tmp arrays */
	double **Stmp = calloc(Ymax, sizeof(double * ));
	double **Itmp = calloc(Ymax, sizeof(double * ));
	double **Rtmp = calloc(Ymax, sizeof(double * ));

	for (int i = 0; i < Ymax; ++i) 
	{
		Stmp[i] = calloc(Xmax, sizeof(double));
		Itmp[i] = calloc(Xmax, sizeof(double));
		Rtmp[i] = calloc(Xmax, sizeof(double));
	}

	/* Fill boundary conditions into tmp arrays */
	for (int i = 0; i < Ymax; ++i) 
	{
		Stmp[i][0] = S[i][0];
		Stmp[i][Xmax - 1] = S[i][Xmax - 1];
		Itmp[i][0] = I[i][0];
		Itmp[i][Xmax - 1] = I[i][Xmax - 1];
		Rtmp[i][0] = R[i][0];
		Rtmp[i][Xmax - 1] = R[i][Xmax - 1];
	}

	for (int j = 0; j < Xmax; ++j) 
	{
		Stmp[0][j] = S[0][j];
		Stmp[Ymax - 1][j] = S[Ymax - 1][j];
		Itmp[0][j] = I[0][j];
		Itmp[Ymax - 1][j] = I[Ymax - 1][j];
		Rtmp[0][j] = R[0][j];
		Rtmp[Ymax - 1][j] = R[Ymax - 1][j];
	}

	int i, j, sweep;

	#pragma omp parallel 
	{
		for (sweep = 0; sweep < nsweeps; sweep += 2) 
		{
			/* Old data in sir; new data in sirtmp */
			#pragma omp for collapse(2) 
			{
				for (i = 1; i < Ymax - 1; ++i) 
				{
					for (j = 1; j < Xmax - 1; ++j) 
					{
						Stmp[i][j] = S[i][j] - beta * S[i][j] * I[i][j] 
							+ dS * (S[i + 1][j] + S[i - 1][j] - 4 * S[i][j] + S[i][j + 1] + S[i][j - 1]);
						Itmp[i][j] = I[i][j] + beta * S[i][j] * I[i][j] - gamma * I[i][j] 
							+ dI * (I[i + 1][j] + I[i - 1][j] - 4 * I[i][j] + I[i][j + 1] + I[i][j - 1]);
						Rtmp[i][j] = R[i][j] + gamma * I[i][j] 
							+ dR * (R[i + 1][j] + R[i - 1][j] - 4 * R[i][j] + R[i][j + 1] + R[i][j - 1]);
					}
				}
			}

			/* Old data in sirtmp; new data in sir */
			#pragma omp for collapse(2) 
			{
				for (i = 1; i < Ymax - 1; ++i) 
				{
					for (j = 1; j < Xmax - 1; ++j) 
					{
						S[i][j] = Stmp[i][j] - beta * Stmp[i][j] * Itmp[i][j] 
							+ dS * (Stmp[i + 1][j] + Stmp[i - 1][j] - 4 * Stmp[i][j] + Stmp[i][j + 1] + Stmp[i][j - 1]);
						I[i][j] = Itmp[i][j] + beta * Stmp[i][j] * Itmp[i][j] - gamma * Itmp[i][j] 
							+ dI * (Itmp[i + 1][j] + Itmp[i - 1][j] - 4 * Itmp[i][j] + Itmp[i][j + 1] + Itmp[i][j - 1]);
						R[i][j] = Rtmp[i][j] + gamma * Itmp[i][j] 
							+ dR * (Rtmp[i + 1][j] + Rtmp[i - 1][j] - 4 * Rtmp[i][j] + Rtmp[i][j + 1] + Rtmp[i][j - 1]);
					}
				}
			}
		}
	}


	free(Stmp);
	free(Itmp);
	free(Rtmp);
}

int main(int argc, char ** argv) 
{
	int Xmax, Ymax, nsteps;
	double beta, gamma, dS, dI, dR;
	double **S, **I, **R;
	char *output_filename;
	timing_t tstart, tend;

	/* Process arguments */
	Xmax = (argc > 1) ? atoi(argv[1]) : 100;
	Ymax = (argc > 2) ? atoi(argv[2]) : 100;
	nsteps = (argc > 3) ? atoi(argv[3]) : 100;
	beta = (argc > 4) ? atoi(argv[4]) : 0.2;
	gamma = (argc > 5) ? atoi(argv[5]) : 0.01;
	dS = (argc > 6) ? atoi(argv[6]) : 0.01;
	dI = (argc > 7) ? atoi(argv[7]) : 0.01;
	dR = (argc > 8) ? atoi(argv[8]) : 0.01;
	output_filename = (argc > 9) ? argv[9] : "../results/output";

	/* Allocate and initialize arrays */
	/* Initialize tmp arrays */
	printf("Initializing Arrays...\n");
	S = calloc(Ymax, sizeof(double * ));
	I = calloc(Ymax, sizeof(double * ));
	R = calloc(Ymax, sizeof(double * ));

	for (int i = 0; i < Ymax; ++i) 
	{
		S[i] = calloc(Xmax, sizeof(double));
		I[i] = calloc(Xmax, sizeof(double));
		R[i] = calloc(Xmax, sizeof(double));
	}

	initialise(S, I, R, Xmax, Ymax);

	/* Run the solver */
	printf("Simulating...\n");
	get_time( & tstart);
	simulate(nsteps, S, I, R, beta, gamma, dS, dI, dR, Xmax, Ymax);
	get_time( & tend);
	printf("Xmax: %d\n"
	"Ymax: %d\n"
	"timesteps: %d\n"
	"Elapsed time: %g s\n",
	Xmax, Ymax, nsteps, timespec_diff(tstart, tend));

	/* Write the I results */
	write_solution(output_filename, Xmax, Ymax, I);

	free(S);
	free(I);
	free(R);
	return 0;
}
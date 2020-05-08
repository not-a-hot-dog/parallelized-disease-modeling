#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

double** read_csv(char const* filename, int Xmax, int Ymax)
{
    char buffer[75000];
    char *record,*line;
    int i=0, j=0;
	//Initialise array
	double ** arr = calloc(Ymax, sizeof(double * ));

	for (int k = 0; k < Ymax; ++k) 
	{
		arr[k] = calloc(Xmax, sizeof(double));
	}

	FILE *fstream = fopen(filename, "r");

    while((line=fgets(buffer,sizeof(buffer),fstream))!=NULL)
    {
        record = strtok(line,",");
        while(record != NULL)
        {
            arr[i][j] = atof(record) ;
            record = strtok(NULL,",");
            ++j;
        }
        ++i ;
        j=0;
    }

	return arr;
}

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

void simulate(int nsweeps, double **S, double **I, double **R, double **beta, 
double **gamma, double **dS, double **dI, double **dR, int Xmax, int Ymax) 
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
						Stmp[i][j] = S[i][j] - beta[i][j] * S[i][j] * I[i][j] 
							+ dS[i][j] * (S[i + 1][j] + S[i - 1][j] - 4 * S[i][j] + S[i][j + 1] + S[i][j - 1]);
						Itmp[i][j] = I[i][j] + beta[i][j] * S[i][j] * I[i][j] - gamma[i][j] * I[i][j] 
							+ dI[i][j] * (I[i + 1][j] + I[i - 1][j] - 4 * I[i][j] + I[i][j + 1] + I[i][j - 1]);
						Rtmp[i][j] = R[i][j] + gamma[i][j] * I[i][j] 
							+ dR[i][j] * (R[i + 1][j] + R[i - 1][j] - 4 * R[i][j] + R[i][j + 1] + R[i][j - 1]);
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
						S[i][j] = Stmp[i][j] - beta[i][j] * Stmp[i][j] * Itmp[i][j] 
						+ dS[i][j] * (Stmp[i + 1][j] + Stmp[i - 1][j] - 4 * Stmp[i][j] + Stmp[i][j + 1] + Stmp[i][j - 1]);
						I[i][j] = Itmp[i][j] + beta[i][j] * Stmp[i][j] * Itmp[i][j] - gamma[i][j] * Itmp[i][j] 
						+ dI[i][j] * (Itmp[i + 1][j] + Itmp[i - 1][j] - 4 * Itmp[i][j] + Itmp[i][j + 1] + Itmp[i][j - 1]);
						R[i][j] = Rtmp[i][j] + gamma[i][j] * Itmp[i][j] 
						+ dR[i][j] * (Rtmp[i + 1][j] + Rtmp[i - 1][j] - 4 * Rtmp[i][j] + Rtmp[i][j + 1] + Rtmp[i][j - 1]);
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
	char *beta_filename, *gamma_filename,
		 *S_init_filename, *I_init_filename, *R_init_filename,
		 *dS_filename, *dI_filename, *dR_filename,
		 *output_filename;
	double tstart, tend;

	/* Process arguments */
	nsteps = (argc > 1) ? atoi(argv[1]) : 100;
	beta_filename = (argc > 2) ? argv[2] : "../data/beta.csv";
	gamma_filename = (argc > 3) ? argv[3] : "../data/gamma.csv";
	S_init_filename = (argc > 4) ? argv[4] : "../data/S_init.csv";
	I_init_filename = (argc > 5) ? argv[5] : "../data/I_init.csv";
	R_init_filename = (argc > 6) ? argv[6] : "../data/R_init.csv";
	dS_filename = (argc > 7) ? atoi(argv[7]) : "../data/dS.csv";
	dI_filename = (argc > 8) ? atoi(argv[8]) : "../data/dI.csv";
	dR_filename = (argc > 9) ? atoi(argv[9]) : "../data/dR.csv";
	output_filename = (argc > 10) ? argv[10] : NULL;
	Xmax = (argc > 11) ? atoi(argv[11]) : 2944;
	Ymax = (argc > 12) ? atoi(argv[12]) : 1792;

    /* Print a diagnostic message */
    #pragma omp parallel
    if (omp_get_thread_num() == 0)
        printf("Threads: %d\n", omp_get_num_threads());

	// initialise(S, I, R, Xmax, Ymax);
	printf("Initializing Arrays...\n");
	double **S = read_csv(S_init_filename, Xmax, Ymax);
	double **I = read_csv(I_init_filename, Xmax, Ymax);
	double **R = read_csv(R_init_filename, Xmax, Ymax);
	printf("Reading Hyperparameters...\n");
	double **dS = read_csv(dS_filename, Xmax, Ymax);
	double **dI = read_csv(dI_filename, Xmax, Ymax);
	double **dR = read_csv(dR_filename, Xmax, Ymax);
	double **beta = read_csv(beta_filename, Xmax, Ymax);
	double **gamma = read_csv(gamma_filename, Xmax, Ymax);

	/* Run the solver */
	printf("Simulating...\n");
	tstart = omp_get_wtime();
	simulate(nsteps, S, I, R, beta, gamma, dS, dI, dR, Xmax, Ymax);
	tend = omp_get_wtime();
	printf("\nXmax: %d\n"
	"Ymax: %d\n"
	"Timesteps: %d\n"
	"\nElapsed Time: %g s\n",
	Xmax, Ymax, nsteps, tend - tstart);

	/* Write the I results */
	if (output_filename)
		write_solution(output_filename, Xmax, Ymax, I);

	free(S);
	free(I);
	free(R);
	free(dS);
	free(dI);
	free(dR);
	free(beta);
	free(gamma);
	return 0;
}
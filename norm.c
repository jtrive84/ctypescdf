/*
Determine the Normal CDF of x given mean mu
and standard deviation sigma.

    `x`     => value for which the normal CDF will be determined
    `mu`    => mean of the corresponding normal distribution
    `sigma` => standard deviation of the corresponding normal distribution
*/
#include <math.h>


double norm_cdf(double x, double mu, double sigma)
{
    double cdf;  // variable to hold result
	double z;    // transformation to standard normal
    const double SQRT_2 = 1.4142135623730951;
    z = (x - mu) / sigma;

    // if x > 3, call erfc; else call erf
    if (x >= 3) {
        cdf = .5 * erfc(- z / SQRT_2);
    }
    else {
        cdf = .5 + .5 * erf(z / SQRT_2);
    }
    return(cdf);
}


/*
For a given array of normal variates, calculate the
corresponding quantile using `norm`.

    `mu`           => mean of the corresponding normal distribution
    `sigma`        => standard deviation of the corresponding normal distribution
    `n`            => the length of input_array/output_array
    `input_array`  => array of inputs (doubles)
    `output_array` => array of computed normal CDFs

*/
void cdf_array(double mu, double sigma, int n,
                double* input_array, double* output_array)
{
    int i;

    // For each element of input_array, call norm
    for (i=0; i<n; i++) {

        output_array[i] = norm_cdf(input_array[i], mu, sigma);

    }
}

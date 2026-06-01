use pyo3::prelude::*;

/// A Python module implemented in Rust.
#[pymodule]
mod glattlibs {
    use pyo3::prelude::*;

    /// Formats the sum of two numbers as string.
    #[pyfunction]
    fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
        Ok((a + b).to_string())
    }

    #[pyfunction]
    fn sum_as_string2(a: usize, b: usize) -> PyResult<String> {
        Ok((a + b).to_string())
    }
}

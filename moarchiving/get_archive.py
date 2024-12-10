""" This module contains the factory functions for creating MOArchive objects
of the appropriate dimensionality, for both constrained and unconstrained problems. """

from moarchiving.moarchiving import BiobjectiveNondominatedSortedList as MOArchive2d
from moarchiving.moarchiving3d import MOArchive3d
from moarchiving.moarchiving4d import MOArchive4d
from moarchiving.constrained_moarchive import CMOArchive

import warnings as _warnings
try:
    import fractions
except ImportError:
    _warnings.warn('`fractions` module not installed, arbitrary precision hypervolume computation not available')


def get_mo_archive(list_of_f_vals=None, reference_point=None, infos=None, n_obj=None):
    """
    Factory function for creating MOArchive objects of the appropriate dimensionality.

    Args:
        list_of_f_vals: list of objective vectors
        reference_point: reference point for the archive
        infos: list of additional information for each objective vector
        n_obj: when initializing an empty archive, the number of objectives should be provided
            to determine the dimensionality of the archive (default is 2)

    Returns:
        MOArchive object of the appropriate dimensionality, based on the number of objectives
    """
    if not hasattr(get_mo_archive, "hypervolume_final_float_type"):
        try:
            get_mo_archive.hypervolume_final_float_type = fractions.Fraction
        except:
            get_mo_archive.hypervolume_final_float_type = float
    if not hasattr(get_mo_archive, "hypervolume_computation_float_type"):
        try:
            get_mo_archive.hypervolume_computation_float_type = fractions.Fraction
        except:
            get_mo_archive.hypervolume_computation_float_type = float

    if (list_of_f_vals is None or len(list_of_f_vals) == 0) and n_obj is None and reference_point is None:
        n_obj = 2

    if n_obj is None:
        if list_of_f_vals is not None and len(list_of_f_vals) > 0:
            n_obj = len(list_of_f_vals[0])
        else:
            n_obj = len(reference_point)

    # check if the number of objectives matches the number of objectives in the list of f_vals
    # and the reference point if they are provided and not empty
    if list_of_f_vals is not None and len(list_of_f_vals) > 0 and reference_point is not None:
        if len(reference_point) != len(list_of_f_vals[0]):
            raise ValueError(f"n_obj ({len(reference_point)}) does not match the number of "
                             f"objectives in the first element of list_of_f_vals "
                             f"({len(list_of_f_vals[0])})")
        elif n_obj != len(list_of_f_vals[0]):
            _warnings.warn(f"n_obj ({n_obj}) does not match the number of objectives in "
                           f"list_of_f_vals ({len(list_of_f_vals[0])})")
            n_obj = len(list_of_f_vals[0])
    elif list_of_f_vals is not None and len(list_of_f_vals) > 0:
        if n_obj != len(list_of_f_vals[0]):
            _warnings.warn(f"n_obj ({n_obj}) does not match the number of objectives in "
                           f"list_of_f_vals ({len(list_of_f_vals[0])})")
            n_obj = len(list_of_f_vals[0])
    elif reference_point is not None:
        if n_obj != len(reference_point):
            _warnings.warn(f"n_obj ({n_obj}) does not match the number of objectives in "
                           f"reference_point ({len(reference_point)})")
            n_obj = len(reference_point)

    if n_obj == 2:
        return MOArchive2d(list_of_f_vals, reference_point=reference_point, infos=infos,
                           hypervolume_final_float_type=get_mo_archive.hypervolume_final_float_type,
                           hypervolume_computation_float_type=get_mo_archive.hypervolume_computation_float_type)
    elif n_obj == 3:
        return MOArchive3d(list_of_f_vals, reference_point=reference_point, infos=infos,
                           hypervolume_final_float_type=get_mo_archive.hypervolume_final_float_type,
                           hypervolume_computation_float_type=get_mo_archive.hypervolume_computation_float_type)
    elif n_obj == 4:
        return MOArchive4d(list_of_f_vals, reference_point=reference_point, infos=infos,
                           hypervolume_final_float_type=get_mo_archive.hypervolume_final_float_type,
                           hypervolume_computation_float_type=get_mo_archive.hypervolume_computation_float_type)
    else:
        raise ValueError(f"Unsupported number of objectives: {n_obj}")


def get_cmo_archive(list_of_f_vals=None, list_of_g_vals=None, reference_point=None,
                    infos=None, n_obj=None, tau=1):
    """
    Function for creating CMOArchive objects, with similar interface as get_mo_archive.

    Args:
        list_of_f_vals: list of objective vectors
        list_of_g_vals: list of constraint vectors, must be the same length as list_of_f_vals
        reference_point: reference point for the archive
        infos: list of additional information for each objective vector
        n_obj: should be provided when initializing an empty archive,
            to determine the dimensionality of the archive (default is 2)
        tau: threshold that indicates when the indicator reaches feasibility
    Returns:
        MOArchive object of the appropriate dimensionality, based on the number of objectives
    """

    if not hasattr(get_cmo_archive, "hypervolume_final_float_type"):
        try:
            get_cmo_archive.hypervolume_final_float_type = fractions.Fraction
        except:
            get_cmo_archive.hypervolume_final_float_type = float
    if not hasattr(get_cmo_archive, "hypervolume_computation_float_type"):
        try:
            get_cmo_archive.hypervolume_computation_float_type = fractions.Fraction
        except:
            get_cmo_archive.hypervolume_computation_float_type = float

    if (list_of_f_vals is None or len(list_of_f_vals) == 0) and n_obj is None and reference_point is None:
        n_obj = 2

    if n_obj is None:
        if list_of_f_vals is not None and len(list_of_f_vals) > 0:
            n_obj = len(list_of_f_vals[0])
        else:
            n_obj = len(reference_point)

    # check if the number of objectives matches the number of objectives in the list of f_vals
    # and the reference point if they are provided and not empty
    if list_of_f_vals is not None and len(list_of_f_vals) > 0 and reference_point is not None:
        if len(reference_point) != len(list_of_f_vals[0]):
            raise ValueError(f"n_obj ({len(reference_point)}) does not match the number of "
                             f"objectives in the first element of list_of_f_vals "
                             f"({len(list_of_f_vals[0])})")
        elif n_obj != len(list_of_f_vals[0]):
            _warnings.warn(f"n_obj ({n_obj}) does not match the number of objectives in "
                           f"list_of_f_vals ({len(list_of_f_vals[0])})")
            n_obj = len(list_of_f_vals[0])
    elif list_of_f_vals is not None and len(list_of_f_vals) > 0:
        if n_obj != len(list_of_f_vals[0]):
            _warnings.warn(f"n_obj ({n_obj}) does not match the number of objectives in "
                           f"list_of_f_vals ({len(list_of_f_vals[0])})")
            n_obj = len(list_of_f_vals[0])
    elif reference_point is not None:
        if n_obj != len(reference_point):
            _warnings.warn(f"n_obj ({n_obj}) does not match the number of objectives in "
                           f"reference_point ({len(reference_point)})")
            n_obj = len(reference_point)

    if list_of_f_vals is None and list_of_g_vals is not None:
        raise ValueError("list_of_f_vals must be provided if list_of_g_vals is provided")
    if list_of_f_vals is not None and list_of_g_vals is None:
        raise ValueError("list_of_g_vals must be provided if list_of_f_vals is provided")
    if list_of_f_vals is not None and list_of_g_vals is not None and len(list_of_f_vals) != len(list_of_g_vals):
        raise ValueError("list_of_f_vals and list_of_g_vals must have the same length")

    return CMOArchive(list_of_f_vals=list_of_f_vals, list_of_g_vals=list_of_g_vals,
                      reference_point=reference_point, infos=infos, n_obj=n_obj, tau=tau,
                      hypervolume_final_float_type=get_cmo_archive.hypervolume_final_float_type,
                      hypervolume_computation_float_type=get_cmo_archive.hypervolume_computation_float_type)

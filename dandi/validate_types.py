from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class ValidationOrigin:
    name: str
    version: str


class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    HINT = "HINT"


class Scope(Enum):
    FILE = "file"
    DANDISET = "dandiset"
    DATASET = "dataset"


@dataclass
class ValidationResult:
    id: str
    origin: ValidationOrigin
    scope: Scope
    # asset_paths, if not populated, assumes [.path], but could be smth like
    # {"path": "task-broken_bold.json",
    #  "asset_paths": ["sub-01/func/sub-01_task-broken_bold.json",
    #                  "sub-02/func/sub-02_task-broken_bold.json"]}
    asset_paths: Optional[List[str]] = None
    # e.g. path within hdf5 file hierarchy
    # As a dict we will map asset_paths into location within them
    within_asset_paths: Optional[Dict[str, str]] = None
    dandiset_path: Optional[Path] = None
    dataset_path: Optional[Path] = None
    # TODO: locations analogous to nwbinspector.InspectorMessage.location
    # but due to multiple possible asset_paths, we might want to have it
    # as a dict to point to location in some or each affected assets
    message: Optional[str] = None
    metadata: Optional[dict] = None
    # ??? should it become a list e.g. for errors which rely on
    # multiple files, like mismatch between .nii.gz header and .json sidecar
    path: Optional[Path] = None
    path_regex: Optional[str] = None
    severity: Optional[Severity] = None

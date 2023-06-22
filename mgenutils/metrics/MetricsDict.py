from typing import Literal, OrderedDict, Union


MetricsName = Union[
    Literal["Precision"],
    Literal["Recall"],
    Literal["F-measure"],
    Literal["Average_Overlap_Ratio"],
    Literal["Precision_no_offset"],
    Literal["Recall_no_offset"],
    Literal["F-measure_no_offset"],
    Literal["Average_Overlap_Ratio_no_offset"],
    Literal["Onset_Precision"],
    Literal["Onset_Recall"],
    Literal["Onset_F-measure"],
    Literal["Offset_Precision"],
    Literal["Offset_Recall"],
    Literal["Offset_F-measure"]
]

MetricsDict = OrderedDict[MetricsName, float]


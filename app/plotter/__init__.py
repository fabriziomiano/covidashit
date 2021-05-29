"""
Plotter class
"""
import io
from base64 import b64encode

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from flask_babel import gettext

from app.data_tools import (
    get_national_data, get_region_data, get_province_data
)
from settings import KEY_PERIODS, REGIONS, PROVINCES
from settings.vars import (
    NEW_POSITIVE_KEY, NEW_POSITIVE_MA_KEY, TOTAL_CASES_KEY, REGION_KEY,
    PROVINCE_KEY, DATE_KEY, VARS
)

plt.rcParams['ytick.labelsize'] = 16
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['font.size'] = 22
plt.rcParams['axes.labelsize'] = 20
plt.rcParams['figure.dpi'] = 96
plt.rcParams['figure.figsize'] = [16, 8]


class Plotter(object):
    """Plotter class to produce matplotlib plot"""

    def __init__(self, varname, data_type, area=None):
        """
        Init class with
        :param varname: str
        :param data_type: str
        :param area: str, optional
        """
        menu = {
            "national": get_national_data,
            "regional": get_region_data,
            "provincial": get_province_data
        }
        self.varname = varname
        self.plot_title = f"{gettext(VARS[self.varname]['title'])}"
        self.area = area
        if self.area:
            filter_key = REGION_KEY if self.area in REGIONS else PROVINCE_KEY
            self.df = menu[data_type](self.area)
            self.df = self.df[self.df[filter_key] == self.area]
            self.plot_title += f" ({self.area})"
        else:
            self.df = menu[data_type]()
        self.df = self.df.set_index(DATE_KEY)

        ax = self.df[self.varname].plot()
        ax.grid(True, linestyle='--', linewidth=.25, color='k')
        ax.set_xlabel('')
        ax.set_ylabel(gettext("Counts"), labelpad=20, weight='bold')
        ax.set_title(self.plot_title)
        ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))

        y_annotation = int(self.df[varname].max() * 0.8)
        if VARS[self.varname]["type"] == "cum":
            y_annotation = int(self.df[varname].max() * 0.1)
            plt.yscale('log')

        ax.tick_params(
            axis="both",
            which="both",
            bottom="off",
            top="off",
            labelbottom="on",
            left="off",
            right="off",
            labelleft="on")
        for key in KEY_PERIODS:
            ax.axvspan(
                KEY_PERIODS[key]["from"],
                KEY_PERIODS[key]["to"],
                alpha=0.5,
                color=KEY_PERIODS[key]["color"])
            ax.annotate(
                KEY_PERIODS[key]["title"],
                xy=(KEY_PERIODS[key]["from"], y_annotation),
                xycoords='data',
                xytext=(-10, 0),
                textcoords='offset points',
                rotation=90,
                fontsize=14)

    @staticmethod
    def to_b64():
        """
        Return a b64 string of the produced plot
        :return: str
        """
        _img = io.BytesIO()
        plt.savefig(_img, format='png', bbox_inches="tight")
        plt.close()
        b64_str = b64encode(_img.getvalue()).decode("utf-8").replace("\n", "")
        return b64_str

    @staticmethod
    def to_bytes():
        """
        Return the byte-content of the produced plot
        :return: str
        """
        _img = io.BytesIO()
        plt.savefig(_img, format='png', bbox_inches="tight")
        plt.close()
        return _img.getvalue()


def validate_plot_request(varname, data_type, area):
    """
    Return a tuple (is_valid: bool, error: str)
    :param varname: str
    :param data_type: str
    :param area: str optional
    :return: tuple
    """
    error = None
    is_valid = False
    available_vars = [var for var in VARS if VARS[var]['type'] != 'vax']
    if varname is None:
        error = (
            "Specify a varname; "
            "Accepted 'varname' for 'national' data_type: [{}]; ".format(
                ", ".join(available_vars))
        )
    elif data_type is None:
        error = "Accepted 'data_type' ['national', 'regional', 'provincial'] "
    else:
        if data_type == "national":
            if varname in VARS:
                if area is None:
                    is_valid = True
                else:
                    error = (
                        "No area should be provided when using "
                        f"data_type=national; remove area={area} "
                        "from query string"
                    )
            else:
                error = (
                    "Accepted 'varname' for 'national' data_type: [{}]; "
                    "".format(", ".join(available_vars)))
        elif data_type == "regional":
            if not area:
                error = "an area must be specified; "
            if area in REGIONS and varname in VARS:
                is_valid = True
            else:
                error = (
                    "Accepted 'varname' for 'regional' data_type: [{}]; "
                    "Accepted 'area' for 'regional' data_type [{}]; "
                    "".format(
                        ", ".join(available_vars),
                        ", ".join([r for r in REGIONS])))
        elif data_type == "provincial":
            available_vars = [
                TOTAL_CASES_KEY, NEW_POSITIVE_KEY, NEW_POSITIVE_MA_KEY]
            if area in PROVINCES and varname in available_vars:
                is_valid = True
            else:
                error = (
                    "Accepted 'varname' for 'provincial' data_type: [{}]; "
                    "Accepted 'area' for 'provincial' data_type [{}]".format(
                        ", ".join([var for var in available_vars]),
                        ", ".join([p for p in PROVINCES])))
        else:
            is_valid = False
            error = (
                "Accepted 'data_type' ['national', 'regional', 'provincial'] ")
    return is_valid, error

from flask_babel import gettext

ITEN_MAP = {
    "ricoverati_con_sintomi": {
        "title": gettext("Hospitalized With Symptoms"),
        "desc": gettext(
            "# of people currently hospitalized with symptoms"
        ),
        "longdesc": gettext(
            "Total count of people currently in hospital "
            "due to coronavirus with symptoms"
        ),
        "icon": "fas fa-hospital-user",
        "increase": {
            "colour": "text-danger",
            "icon": "fas fa-long-arrow-alt-up",
            "tooltip": gettext("Increased with respect to yesterday")
        },
        "decrease": {
            "colour": "text-success",
            "icon": "fas fa-long-arrow-alt-down",
            "tooltip": gettext("Decreased with respect to yesterday")
        },
        "stable": {
            "colour": "text-info",
            "icon": "fas fa-minus",
            "tooltip": gettext("Stable with respect to yesterday")
        }
    },
    "terapia_intensiva": {
        "title": gettext("Intensive Care Unit"),
        "desc": gettext("# of people currently in ICU"),
        "longdesc": gettext(
            "Total count of people currently in ICU and positive to COVID-19"
        ),
        "icon": "fas fa-procedures",
        "increase": {
            "colour": "text-danger",
            "icon": "fas fa-long-arrow-alt-up",
            "tooltip": gettext("Increased with respect to yesterday")
        },
        "decrease": {
            "colour": "text-success",
            "icon": "fas fa-long-arrow-alt-down",
            "tooltip": gettext("Decreased with respect to yesterday")
        },
        "stable": {
            "colour": "text-info",
            "icon": "fas fa-minus",
            "tooltip": gettext("Stable with respect to yesterday")
        }
    },
    "totale_ospedalizzati": {
        "title": gettext("Total Hospitalized"),
        "desc": gettext("# of people currently hospitalized"),
        "longdesc": gettext(
            "Total count of people currently hospitalized. "
            "It takes into account ICU"),
        "icon": "fas fa-hospital-user",
        "increase": {
            "colour": "text-danger",
            "icon": "fas fa-long-arrow-alt-up",
            "tooltip": gettext("Increased with respect to yesterday")
        },
        "decrease": {
            "colour": "text-success",
            "icon": "fas fa-long-arrow-alt-down",
            "tooltip": gettext("Decreased with respect to yesterday")
        },
        "stable": {
            "colour": "text-info",
            "icon": "fas fa-minus",
            "tooltip": gettext("Stable with respect to yesterday")
        }
    },
    "isolamento_domiciliare": {
        "title": gettext("Self Isolation"),
        "desc": gettext("# of people currently in self isolation"),
        "longdesc": gettext(
            "People currently positive but who don't need hospitalization"
        ),
        "icon": "fas fa-house-user",
        "increase": {
            "colour": "text-danger",
            "icon": "fas fa-long-arrow-alt-up",
            "tooltip": gettext("Increased with respect to yesterday")
        },
        "decrease": {
            "colour": "text-success",
            "icon": "fas fa-long-arrow-alt-down",
            "tooltip": gettext("Decreased with respect to yesterday")
        },
        "stable": {
            "colour": "text-info",
            "icon": "fas fa-minus",
            "tooltip": gettext("Stable with respect to yesterday")
        }
    },
    "totale_positivi": {
        "title": gettext("Total Positive"),
        "desc": gettext(
            "# of people currently "
            "hospitalized with symptoms + ICU + self isolation"
        ),
        "longdesc": gettext(
            "People currently positive. "
            "Unlike 'Total Cases' it does not take into account "
            "'healed' and 'deaths'. By the end of the outbreak "
            "this should tend to zero. In particular, it is: "
            "total positive = total cases - total healed - total deaths"
        ),
        "icon": "fas fa-viruses",
        "increase": {
            "colour": "text-danger",
            "icon": "fas fa-long-arrow-alt-up",
            "tooltip": gettext("Increased with respect to yesterday")
        },
        "decrease": {
            "colour": "text-success",
            "icon": "fas fa-long-arrow-alt-down",
            "tooltip": gettext("Decreased with respect to yesterday")
        },
        "stable": {
            "colour": "text-info",
            "icon": "fas fa-minus",
            "tooltip": gettext("Stable with respect to yesterday")
        }
    },
    "variazione_totale_positivi": {
        "title": gettext("Total Positive Variation"),
        "desc": gettext(
            "Variation of # of people currently positive "
            "with respect to yesterday"
        ),
        "longdesc": gettext(
            "Variation of the number of people currently positive "
            "with respect to the previous day. It is negative when the number "
            "of daily healed and deaths is larger than 'New positive'"
        ),
        "icon": "fas fa-chart-area",
        "increase": {
            "colour": "text-danger",
            "icon": "fas fa-long-arrow-alt-up",
            "tooltip": gettext("Increased with respect to yesterday")
        },
        "decrease": {
            "colour": "text-success",
            "icon": "fas fa-long-arrow-alt-down",
            "tooltip": gettext("Decreased with respect to yesterday")
        },
        "stable": {
            "colour": "text-info",
            "icon": "fas fa-minus",
            "tooltip": gettext("Stable with respect to yesterday")
        }
    },
    "nuovi_positivi": {
        "title": gettext("New Positive"),
        "desc": gettext("Daily count of new positve cases"),
        "longdesc": gettext("Daily count of new positve cases"),
        "icon": "fas fa-virus",
        "increase": {
            "colour": "text-danger",
            "icon": "fas fa-long-arrow-alt-up",
            "tooltip": gettext("Increased with respect to yesterday")
        },
        "decrease": {
            "colour": "text-success",
            "icon": "fas fa-long-arrow-alt-down",
            "tooltip": gettext("Decreased with respect to yesterday")
        },
        "stable": {
            "colour": "text-info",
            "icon": "fas fa-minus",
            "tooltip": gettext("Stable with respect to yesterday")
        }
    },
    "dimessi_guariti": {
        "title": gettext("Total Healed"),
        "desc": gettext("Cumulative # of people healed"),
        "longdesc": gettext(
            "Total number of people healed since the beginning of the outbreak"
        ),
        "icon": "far fa-smile",
        "increase": {
            "colour": "text-success",
            "icon": "fas fa-long-arrow-alt-up",
            "tooltip": gettext("Increased with respect to yesterday")
        },
        "decrease": {
            "colour": "text-danger",
            "icon": "fas fa-long-arrow-alt-down",
            "tooltip": gettext("Decreased with respect to yesterday")
        },
        "stable": {
            "colour": "text-info",
            "icon": "fas fa-minus",
            "tooltip": gettext("Stable with respect to yesterday")
        }
    },
    "deceduti": {
        "title": gettext("Total Deaths"),
        "desc": gettext("Total deaths count"),
        "longdesc": gettext(
            "Total deaths count since the beginning of the outbreak"
        ),
        "icon": "fas fa-cross",
        "increase": {
            "colour": "text-danger",
            "icon": "fas fa-long-arrow-alt-up",
            "tooltip": gettext("Increased with respect to yesterday")
        },
        "decrease": {
            "colour": "text-success",
            "icon": "fas fa-long-arrow-alt-down",
            "tooltip": gettext("Decreased with respect to yesterday")
        },
        "stable": {
            "colour": "text-info",
            "icon": "fas fa-minus",
            "tooltip": gettext("Stable with respect to yesterday")
        }
    },
    "totale_casi": {
        "title": gettext("Total Cases"),
        "desc": gettext(
            "Total count of the positive tests since the"
            " beginning of the outbreak"
        ),
        "longdesc": gettext(
            "Total count of the positive tests since the"
            " beginning of the outbreak"
        ),
        "icon": "fas fa-viruses",
        "increase": {
            "colour": "text-danger",
            "icon": "fas fa-long-arrow-alt-up",
            "tooltip": gettext("Increased with respect to yesterday")
        },
        "decrease": {
            "colour": "text-success",
            "icon": "fas fa-long-arrow-alt-down",
            "tooltip": gettext("Decreased with respect to yesterday")
        },
        "stable": {
            "colour": "text-info",
            "icon": "fas fa-minus",
            "tooltip": gettext("Stable with respect to yesterday")
        }
    },
    "tamponi": {
        "title": gettext("Total Swabs"),
        "desc": gettext("# of swabs performed"),
        "longdesc": gettext(
            "Total number of swabs performed since the beginning of the outbreak"
        ),
        "icon": "fas fa-vial",
        "increase": {
            "colour": "text-danger",
            "icon": "",
            "tooltip": gettext("Increased with respect to yesterday")
        },
        "decrease": {
            "colour": "text-success",
            "icon": "",
            "tooltip": gettext("Decreased with respect to yesterday")
        },
        "stable": {
            "colour": "text-info",
            "icon": "",
            "tooltip": gettext("Stable with respect to yesterday")
        }
    },
    "deceduti_giornalieri": {
        "title": gettext("Daily deaths"),
        "desc": gettext("Daily deaths count"),
        "longdesc": gettext("Daily deaths count"),
        "icon": "fas fa-cross",
        "increase": {
            "colour": "text-danger",
            "icon": "fas fa-long-arrow-alt-up",
            "tooltip": gettext("Increased with respect to yesterday")
        },
        "decrease": {
            "colour": "text-success",
            "icon": "fas fa-long-arrow-alt-down",
            "tooltip": gettext("Decreased with respect to yesterday")
        },
        "stable": {
            "colour": "text-info",
            "icon": "fas fa-minus",
            "tooltip": gettext("Stable with respect to yesterday")
        }
    }
}
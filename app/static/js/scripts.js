let PROVINCES = [
    'Agrigento', 'Alessandria', 'Ancona', 'Aosta', 'Arezzo',
    'Ascoli Piceno', 'Asti', 'Avellino', 'Bari',
    'Barletta-Andria-Trani', 'Belluno', 'Benevento', 'Bergamo',
    'Biella', 'Bologna', 'Bolzano', 'Brescia', 'Brindisi', 'Cagliari',
    'Caltanissetta', 'Campobasso', 'Caserta', 'Catania', 'Catanzaro',
    'Chieti', 'Como', 'Cosenza', 'Cremona', 'Crotone', 'Cuneo',
    'Enna', 'Fermo', 'Ferrara', 'Firenze', 'Foggia', 'Forlì-Cesena',
    'Frosinone', 'Genova', 'Gorizia', 'Grosseto', 'Imperia',
    'Isernia', "L'Aquila", 'La Spezia', 'Latina', 'Lecce', 'Lecco',
    'Livorno', 'Lodi', 'Lucca', 'Macerata', 'Mantova',
    'Massa Carrara', 'Matera', 'Messina', 'Milano', 'Modena',
    'Monza e della Brianza', 'Napoli', 'Novara', 'Nuoro', 'Oristano',
    'Padova', 'Palermo', 'Parma', 'Pavia', 'Perugia',
    'Pesaro e Urbino', 'Pescara', 'Piacenza', 'Pisa', 'Pistoia',
    'Pordenone', 'Potenza', 'Prato', 'Ragusa', 'Ravenna',
    'Reggio di Calabria', "Reggio nell'Emilia", 'Rieti', 'Rimini',
    'Roma', 'Rovigo', 'Salerno', 'Sassari', 'Savona', 'Siena',
    'Siracusa', 'Sondrio', 'Sud Sardegna', 'Taranto', 'Teramo',
    'Terni', 'Torino', 'Trapani', 'Trento', 'Treviso', 'Trieste',
    'Udine', 'Varese', 'Venezia', 'Verbano-Cusio-Ossola', 'Vercelli',
    'Verona', 'Vibo Valentia', 'Vicenza', 'Viterbo'
];

let REGIONS = [
    'Abruzzo', 'Basilicata', 'Calabria', 'Campania', 'Emilia-Romagna',
    'Friuli Venezia Giulia', 'Lazio', 'Liguria', 'Lombardia',
    'Marche', 'Molise', 'P.A. Bolzano', 'P.A. Trento', 'Piemonte',
    'Puglia', 'Sardegna', 'Sicilia', 'Toscana', 'Umbria',
    "Valle d'Aosta", 'Veneto'
];

let AREAS = REGIONS.concat(PROVINCES);

let URL_REGIONS = '/regions/';
let URL_PROVINCES = '/provinces/';

let SEARCHERRMSG = '{{ gettext("Region/province not in the right format") }}';

(function ($) {
    "use strict";

    // Add active state to sidebar nav links
    const path = window.location.href; // because the 'href' property of the DOM element is the absolute path
    $("#layoutSidenav_nav .sb-sidenav a.nav-link").each(function () {
        if (this.href === path) {
            $(this).addClass("active");
        }
    });

    // Toggle the side navigation
    $("#sidebarToggle").on("click", function (e) {
        e.preventDefault();
        $("body").toggleClass("sb-sidenav-toggled");
        $(window).resize();
    });

    // activate tooltips
    $(function () {
        $('[data-toggle="tooltip"]').tooltip();
    })

    // activate data tables
    $(function () {
        $('[class="table table-bordered"]').DataTable({
            "order": [[1, "desc"]]
        })
    })


    $(function () {
        if ((window.location.href.includes("provinces")) || (window.location.href.includes("regions"))) {
            $("#areasCollapse").addClass('active');
            $("#areasDiv").addClass("text-success");

        } else {
            $("#nationalDataDiv").addClass("text-danger");
        }
    })

    $(function () {
        $('#searchInput').autocomplete({
            source: AREAS,
            delay: 0,
            autoFocus: true,
            select: function (event, ui) {
                document.location.href = validateSearchInput(ui.item.value);
            },
            focus: function (event) {
                event.preventDefault();
            }
        });
    });

    $(function () {
        $("#searchInput").on('change', function (e) {
            e.preventDefault();
            let url = validateSearchInput($("#searchInput").val());
            $("#searchForm").removeAttr('action').attr('action', url);
        })
    })

    function validateSearchInput(searchInput) {
        let url = "";
        console.log(searchInput)
        if (REGIONS.includes(searchInput)) {
            url = URL_REGIONS + searchInput;
        } else if (PROVINCES.includes(searchInput)) {
            url = URL_PROVINCES + searchInput;
        } else {
            alert(SEARCHERRMSG);
        }
        return url;
    }

})(jQuery);


/*Scroll to top when arrow up clicked BEGIN*/
$(window).scroll(function () {
    let height = $(window).scrollTop();
    if (height > 100) {
        $('#back2Top').fadeIn();
    } else {
        $('#back2Top').fadeOut();
    }
});

$(document).ready(function () {
    $("#back2Top").click(function (event) {
        event.preventDefault();
        $("html, body").animate({ scrollTop: 0 }, "slow");
        return false;
    });

});

// check on new users
$(document).ready(function () {
    let hasVisited = localStorage.getItem("hasVisited");
    let localVersion = localStorage.getItem("version");
    if (hasVisited === null || localVersion !== VERSION ) {
        $('#welcomeModal').modal('show');
        hasVisited = "yes"; // localStorage.setItem() only accepts strings
        localStorage.setItem("hasVisited", hasVisited);
        localStorage.setItem("version", VERSION);
    }
});

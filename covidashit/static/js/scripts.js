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


(function ($) {
    "use strict";

    // highlight the currently active UI
    const path = window.location.href;
    $("#topNav a.nav-link").each(function () {
        if (this.href === path) {
            $(this).addClass("active");
        }
        if (path.includes("regions") || path.includes("provinces")) {
            $("#pandemicNavLink").addClass("active");
        }
        if (path.includes("vaccines")) {
            $("#vaccinesNavLink").addClass("active");
        }
    });

    $(function () {
        if ((window.location.href.includes("provinces")) || (window.location.href.includes("regions"))) {
            $("#areasCollapse").addClass('active');
            $("#areasDiv").addClass("text-success");

        } else {
            $("#nationalDataDiv").addClass("text-danger");
        }
    })

    // search-input autocomplete
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

    // search-input functionality
    $(function () {
        $("#searchInput").on('submit', function (e) {
            e.preventDefault();
            let url = validateSearchInput($("#searchInput").val());
            $("#searchForm").removeAttr('action').attr('action', url);
        })
    })

    // validate search input
    function validateSearchInput(searchInput) {
        let url = "";
        console.log(searchInput)
        if (REGIONS.includes(searchInput)) {
            url = URL_REGIONS + searchInput;
        } else if (PROVINCES.includes(searchInput)) {
            url = URL_PROVINCES + searchInput;
        } else {
            let err_msg = "Please Choose one from the list";
            alert(err_msg);
        }
        return url;
    }

    // back-to-top functionality
    $(window).scroll(function () {
        let height = $(window).scrollTop();
        if (height > 100) {
            $('#back2Top').fadeIn();
        } else {
            $('#back2Top').fadeOut();
        }
    });

    $(document).ready(function () {

        // back-to-top button
        $("#back2Top").click(function (event) {
            event.preventDefault();
            $("html, body").animate({ scrollTop: 0 }, "slow");
            return false;
        });

        // check if new user
        let hasVisited = localStorage.getItem("hasVisited");
        let localVersion = localStorage.getItem("version");
        if (hasVisited === null || localVersion !== VERSION) {
            $('#welcomeModal').modal('show');
            hasVisited = "yes"; // localStorage.setItem() only accepts strings
            localStorage.setItem("hasVisited", hasVisited);
            localStorage.setItem("version", VERSION);
        }

        // enable chosen
        $('[class="chosen"]').chosen();
        $(".chosen-select").chosen({ max_selected_options: 3 });

        // enable BS tooltips
        $('[data-toggle="tooltip"]').tooltip()
    });

})(jQuery);

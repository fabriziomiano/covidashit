let provinces = [
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

let regions = [
    'Abruzzo', 'Basilicata', 'Calabria', 'Campania', 'Emilia-Romagna',
    'Friuli Venezia Giulia', 'Lazio', 'Liguria', 'Lombardia',
    'Marche', 'Molise', 'P.A. Bolzano', 'P.A. Trento', 'Piemonte',
    'Puglia', 'Sardegna', 'Sicilia', 'Toscana', 'Umbria',
    "Valle d'Aosta", 'Veneto'
];

let regionsAndProvinces = regions.concat(provinces);

let regionsUrl = '/regions/';
let provincesUrl = '/provinces/';


(function ($) {
    "use strict";

    // Add active state to sidbar nav links
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
            source: regionsAndProvinces,
            delay: 0,
            autoFocus: true,
            select: function (event, ui) {
                document.location.href = validateSearchInput(ui.item.value);
            },
            focus: function (event, ui) {
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
        if (regions.includes(searchInput)) {
            url = regionsUrl + searchInput;
        } else if (provinces.includes(searchInput)) {
            url = provincesUrl + searchInput;
        } else {
            alert(searchInputErrMsg);
        }
        return url;
    }

})(jQuery);

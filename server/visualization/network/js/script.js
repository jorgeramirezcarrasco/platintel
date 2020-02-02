am4core.ready(function () {

    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    var chart = am4core.create("chartdiv", am4plugins_forceDirected.ForceDirectedTree);
    var networkSeries = chart.series.push(new am4plugins_forceDirected.ForceDirectedSeries())

    chart.data = [
        {
            name: "#Op2020",
            value: 500,
            children: [{
                'name': '@anons_fw',
                'value': '',
                'collapsed': 'true',
                'children': [{
                    'name': 'twitter.com/anons_fw/status/1218626256389971974',
                    'value': 0
                }]
            },
            {
                'name': '@H0t31Y0rb4',
                'value': '',
                'collapsed': 'true',
                'children': [{
                    'name': 'twitter.com/H0t31Y0rb4/status/1215452152199634944',
                    'value': 4
                },
                { 'name': 'twitter.com/H0t31Y0rb4/status/1215452095534354432', 'value': 3 }]
            },
            {
                'name': '@AnonymousJota',
                'value': '',
                'collapsed': 'true',
                'children': [{
                    'name': 'twitter.com/AnonymousJota/status/1215380437838761984',
                    'value': 1
                }]
            },
            {
                'name': '@PequeFran',
                'value': '',
                'collapsed': 'true',
                'children': [{
                    'name': 'twitter.com/PequeFran/status/1215270467726192642',
                    'value': 1
                }]
            },
            {
                'name': '@fs_lda',
                'value': '',
                'collapsed': 'true',
                'children': [{
                    'name': 'twitter.com/fs_lda/status/1215125677986455552',
                    'value': 0
                }]
            },
            {
                'name': '@CristianARN_cl',
                'value': '',
                'collapsed': 'true',
                'children': [{
                    'name': 'twitter.com/CristianARN_cl/status/1215110261385895936',
                    'value': 4
                }]
            },
            {
                'name': '@Anonymous196307',
                'value': '',
                'collapsed': 'true',
                'children': [{
                    'name': 'twitter.com/Anonymous196307/status/1212535558984982528',
                    'value': 16
                }]
            },
            {
                'name': '@flor_nicola',
                'value': '',
                'collapsed': 'true',
                'children': [{
                    'name': 'twitter.com/flor_nicola/status/1212441329193631745',
                    'value': 1
                }]
            },
            {
                'name': '@ChalecosAmarill',
                'value': '',
                'collapsed': 'true',
                'children': [{
                    'name': 'twitter.com/ChalecosAmarill/status/1212436496592048138',
                    'value': 716
                },
                {
                    'name': 'twitter.com/ChalecosAmarill/status/1212139120354562048',
                    'value': 36
                }]
            },
            {
                'name': '@natyvem',
                'value': '',
                'collapsed': 'true',
                'children': [{
                    'name': 'twitter.com/natyvem/status/1212133881295593474',
                    'value': 0
                }]
            },
            {
                'name': '@paograndon',
                'value': '',
                'collapsed': 'true',
                'children': [{
                    'name': 'twitter.com/paograndon/status/1212064871233310720',
                    'value': 0
                }]
            },
            {
                'name': '@17Fabix',
                'value': '',
                'collapsed': 'true',
                'children': [{
                    'name': 'twitter.com/17Fabix/status/1211998265878679553',
                    'value': 0
                }]
            },
            {
                'name': '@AnonymousIbero',
                'value': '',
                'collapsed': 'true',
                'children': [{
                    'name': 'twitter.com/AnonymousIbero/status/1211476021872091136',
                    'value': 33
                }]
            },
            {
                'name': '@IberoAnonOps',
                'value': '',
                'collapsed': 'true',
                'children': [{
                    'name': 'twitter.com/IberoAnonOps/status/1211475339852931072',
                    'value': 16
                }]
            },
            {
                'name': '@AnonPegaso',
                'value': '',
                'collapsed': 'true',
                'children': [{
                    'name': 'twitter.com/AnonPegaso/status/1211341744094302212',
                    'value': 21
                }]
            },
            {
                'name': '@immellocker',
                'value': '',
                'collapsed': 'true',
                'children': [{
                    'name': 'twitter.com/immellocker/status/1116254408646496256',
                    'value': 0
                }]
            },
            {
                'name': '@CitizenoftheWo4',
                'value': '',
                'collapsed': 'true',
                'children': [{
                    'name': 'twitter.com/CitizenoftheWo4/status/1026197881374404611',
                    'value': 1
                },
                {
                    'name': 'twitter.com/CitizenoftheWo4/status/1022173461106458624',
                    'value': 0
                }]
            },
            {
                'name': '@Sajkoo',
                'value': '',
                'collapsed': 'true',
                'children': [{
                    'name': 'twitter.com/Sajkoo/status/782167161460654080',
                    'value': 0
                }]
            }]
        }
    ];


    networkSeries.dataFields.value = "value";
    networkSeries.dataFields.name = "name";
    networkSeries.dataFields.children = "children";
    networkSeries.dataFields.collapsed = "collapsed";

    networkSeries.nodes.template.tooltipText = "{name}";
    networkSeries.nodes.template.fillOpacity = 1;
    networkSeries.manyBodyStrength = -20;
    networkSeries.links.template.strength = 0.8;
    networkSeries.minRadius = am4core.percent(2);
    networkSeries.nodes.template.events.on("hit", function (ev) {
        if (ev.target.dataItem.name.includes("twitter")) {
            window.open("https://" + ev.target.dataItem.name, '_blank');
        }
    });

    networkSeries.nodes.template.label.text = "{name}"
    networkSeries.fontSize = 10;

}); // end am4core.ready()

function toTitleCase(str)
{
    return str.replace(/([^\W_]+[^\s-]*) */g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

// enable modal windows
function show_modal(title, body)
{
    $("#page-modal-title").html(title);
    $("#page-modal-body").html(body);
    $("#page-modal").modal({'show': true});
}

function readable_attr(attr_name)
{
    return toTitleCase(attr_name.replace("_", " "))
}

function map_model_to_modal(model, title_attr, display_attrs)
{
    var title = model[title_attr]
    var body = ""

    for (var i=0; i<display_attrs.length; i++)
    {
        console.log(model[display_attrs[i]])
        if(model[display_attrs[i]])
        {
            var key = display_attrs[i]
            var value = model[display_attrs[i]]
            body += readable_attr(key) + " " + value + "<br>"
        }
    }
    show_modal(title, body)
}

function show_supplier_modal(supplier)
{
    var attrs = [
        'street_address',
        'website',
        'contact',
        'phone',
        'alt_phone',
        'fax',
        'email',
        'alt_email',
        'added_by'
    ]
    map_model_to_modal(supplier, 'name', attrs)
}

function show_manufacturer_modal(manufacturer)
{
    var attrs = [
        'name',
        'country_name'
    ]
    manufacturer['country_name'] = manufacturer.country.name
    map_model_to_modal(manufacturer, 'name', attrs)
}

$(document).ready(function(){

    // enable tooltips
    $(".tooltip-enabled").tooltip({});

    // handle search
    $("#search-box").typeahead({
        minLength: 1,
        source:function(query, process){
            medicines = [];
            map = {};
            $.get(API_HOST + 'autocomplete/' + query + '/', function(data){
                for (var i = 0; i < data.length; i++)
                {
                    var key = data[i].name;
                    if (key)
                        medicines.push(key)
                    map[key] = data[i]
                }
                process(medicines);
            },'json');
        },
        updater: function (item) {
            window.location = '/medicine/' + map[item].medicine_id.toString() + '/';
            return item;
        },
        matcher: function (item) {
            // matching's done on the backend
            return true
        }
    });
    $("#search-box").focus()

});
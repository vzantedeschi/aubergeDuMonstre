/* Handlebars */
loadTemplate = function(template_id) {
    var source = $(template_id).html();
    return Handlebars.compile(source);
}
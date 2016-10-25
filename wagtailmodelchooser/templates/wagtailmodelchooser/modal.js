function initModal(modal) {

    /**
     * Attach event handlers to the links
     */
    function ajaxifyLinks(context) {
        $('a.model-choice', modal.body).click(function(e) {
            e.preventDefault();
            var instance = $(this);
            modal.respond('instanceChosen', {
                'string': instance.text(),
                'pk': instance.data('pk'),
            });
            modal.close();
        });

        $('.pagination a', context).click(function(e) {
            e.preventDefault();
            var page = this.getAttribute('data-page');
            setPage(page);
        });
    }

    ajaxifyLinks(modal.body);

    /**
     * Search the list
     */
    var searchForm = modal.body.find('form.search-bar');
    var searchField = searchForm.find('#id_q');
    var searchUrl = searchForm.attr('action');
    var searchResults = modal.body.find('#search-results');
    function search() {
        loadResults(searchField.val())
    }

    searchForm.submit(search);
    var searchFieldChange = function(e) {
        clearTimeout($.data(this, 'timer'));
        var wait = setTimeout(search, 100);
        $(this).data('timer', wait);
    }
    searchForm.on('input', searchFieldChange);
    searchForm.on('change', searchFieldChange);
    searchForm.on('keyup', searchFieldChange);

    /**
     * Load page number ``page`` of the results.
     */
    function setPage(page) {
        loadResults(searchField.val(), page)
    }

    /**
     * Actually do the work
     */
    function loadResults(searchTerm, page) {
        var dataObj = {ajax: 1}
        if (window.instance) dataObj['instance'] = window.instance;
        if (searchTerm) dataObj['q'] = searchTerm;
        if (page) dataObj['p'] = page;

        $.ajax({
            url: searchUrl,
            data: dataObj,
            success: function(data, status) {
                console.log(data, status);
                searchResults.html(data);
                ajaxifyLinks(searchResults);
            }
        });
    }
}

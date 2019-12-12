(function() {
/**
 * Once the model chooser modal has appeared, register the event
 * listeners we need for that.
 */
function setupModal(modal, jsonData) {
    /**
     * Attach event handlers to the results. A live listener
     * because we replace the modal contents with Ajax.
     */
    modal.body.on('click', 'a.model-choice', function(e) {
        e.preventDefault();
        var instance = $(this);
        modal.respond('instanceChosen', {
            'string': instance.text(),
            'pk': instance.data('pk'),
        });
        modal.close();
    });

    /**
     * Handle pagination links. A live listener because we
     * replace the modal content with Ajax.
     */
    modal.body.on('click', '.pagination a', function(e) {
        e.preventDefault();
        var page = this.getAttribute('data-page');
        setPage(page);
    });

    /**
     * Search the list
     */
    var searchForm = modal.body.find('form.search-bar');
    var searchField = searchForm.find('#id_q');
    var searchUrl = searchForm.attr('action');
    var searchResults = modal.body.find('#search-results');
    function search() {
        loadResults(searchField.val());

        // We want to deal with the form in javascript without submitting
        // the page
        return false;
    }

    searchForm.submit(search);
    var searchFieldChange = function(e) {
        clearTimeout($.data(this, 'timer'));
        var wait = setTimeout(search, 250);
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
                searchResults.html(data);
                ajaxifyLinks(searchResults);
            }
        });
    }
}

/**
 * Registers the javascript hooks needed by the Wagtail admin
 * 'choose <model>' button.
 */
function setupWagtailWidget(id, url) {
    var chooserElement = $('#' + id + '-chooser');
    var title = chooserElement.find('.title');
    var input = $('#' + id);

    chooserElement.find('.action-choose').click(function() {
        ModalWorkflow({
            url: url,
            onload: {
                'show_model_chooser': setupModal
            },
            responses: {
                instanceChosen: function(instanceData) {
                    input.val(instanceData.pk);
                    title.text(instanceData.string);
                    chooserElement.removeClass('blank');
                }
            }
        });
    });

    $('.action-clear', chooserElement).click(function() {
        input.val('');
        chooserElement.addClass('blank');
    });
}

/**
 * Register a global function to be called when our model chooser widget
 * is rendered in Wagtail admin.
 */
window.createModelChooser = setupWagtailWidget;
})();

(function() {
/**
 * Public API for the modal
 */
function ModelChooser() {
    this.hooks = {
        "setup": [],
        "choose": [],
        "ajax": [],
    };
}

/**
 * Register a function to be called when the modal is visible. Allows
 * you to register any additional javascript needed.
 */
ModelChooser.prototype.addSetupHook = function addSetupHook(hook) {
    this.hooks["setup"].push(hook);
};

/**
 * Register a function to be called once an instance is chosen. Return
 * true to choose the instance, or false to block.
 */
ModelChooser.prototype.addChooseHook = function addChooseHook(hook) {
    this.hooks["choose"].push(hook);
};

/**
 * Register a function to be called just before ajax requests. Return
 * a dictionary of parameters, or null to cancel the request.
 */
ModelChooser.prototype.addAjaxHook = function addAjaxHook(hook) {
    this.hooks["ajax"].push(hook);
};

/**
 * Once the model chooser modal has appeared, register the event
 * listeners we need for that.
 */
ModelChooser.prototype.setupModal = function setupModal(modal, jsonData) {
    var that = this;

    /**
     * Attach event handlers to the results. A live listener
     * because we replace the modal contents with Ajax.
     */
    modal.body.on('click', 'a.model-choice', function(e) {
        e.preventDefault();
        var instance = $(this);

        // Call choose hooks
        for (var i=0;i<that.hooks["choose"].length;i++) {
            var hook = that.hooks["choose"][i];

            // Allow mutation of params
            var result = hook.call(that, modal, instance);
            if (!result) {
                // Block choice
                return;
            }
        }

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
    var searchUrl = searchForm.attr('action');
    var searchResults = modal.body.find('#search-results');
    // Builds a dictionary of the values of fields in searchForm
    function buildSearchDict() {
        var rtn = {};
        searchForm.find("input, select, textarea").each(function() {
            var elm = $(this);
            if (elm.is("input[type=checkbox], input[type=radio]")) {
                if (elm.prop("checked")) {
                    rtn[elm.attr("name")] = elm.val();
                } else {
                    // Unchecked, don't record it
                }
            } else {
                rtn[elm.attr("name")] = elm.val();
            }
        });

        return rtn;
    }

    function search() {
        loadResults(buildSearchDict());

        // We want to deal with the form in javascript without submitting
        // the page
        return false;
    }

    // Call setup hooks
    $.each(that.hooks["setup"], function(_, hook) {
        hook.call(that, modal);
    });

    searchForm.submit(search);
    var searchChange = function(e) {
        clearTimeout($.data(this, 'timer'));
        var wait = setTimeout(search, 250);
        $(this).data('timer', wait);
    }
    searchForm.on('input', searchChange);
    searchForm.on('change', searchChange);
    searchForm.on('keyup', searchChange);

    /**
     * Load page number ``page`` of the results.
     */
    function setPage(page) {
        loadResults(buildSearchDict(), page)
    }

    /**
     * Actually do the work
     */
    function loadResults(searchFields, page) {
        var dataObj = {ajax: 1}
        if (window.instance) dataObj['instance'] = window.instance;
        if (page) dataObj['p'] = page;

        var params = $.extend(dataObj, searchFields);

        // Call ajax hooks
        for (var i=0;i<that.hooks["ajax"].length;i++) {
            var hook = that.hooks["ajax"][i];

            // Allow mutation of params
            params = hook.call(that, modal, params);
            if (params == null) {
                // Block request
                return;
            }
        }

        $.ajax({
            url: searchUrl,
            data: params,
            success: function(data, status) {
                searchResults.html(data);
            }
        });
    }
};

/**
 * Registers the javascript hooks needed by the Wagtail admin
 * 'choose <model>' button.
 */
ModelChooser.prototype.setupWagtailWidget = function setupWagtailWidget(id, url) {
    var that = this;
    var chooserElement = $('#' + id + '-chooser');
    var title = chooserElement.find('.title');
    var input = $('#' + id);

    // Construct initial state of the chooser from the rendered (static) HTML;
    // this is either null (no item chosen) or a dict of id and display_title
    var state = null;
    if (input.val()) {
        state = {
            id: input.val(),
            display_title: title.text()
        };
    }

    // define public API functions for the chooser:
    // https://docs.wagtail.io/en/latest/reference/streamfield/widget_api.html
    var chooser = {
        getState: function() { return state; },
        getValue: function() { return state && state.id; },
        setState: function(newState) {
            if (newState) {
                input.val(newState.id);
                title.text(newState.display_title);
                chooserElement.removeClass('blank');
            } else {
                input.val('');
                chooserElement.addClass('blank');
            }
            state = newState;
        },
        clear: function() {
            chooser.setState(null);
        },
        getTextLabel: function(opts) {
            if (!state) return null;
            var result = state.display_title;
            if (opts && opts.maxLength && result.length > opts.maxLength) {
                return result.substring(0, opts.maxLength - 1) + '…';
            }
            return result;
        },
        focus: () => {
            chooserElement.find('.action-choose').focus();
        },
        openChooserModal: function() {
            ModalWorkflow({
                url: url,
                onload: {
                    'show_model_chooser': that.setupModal.bind(that)
                },
                responses: {
                    instanceChosen: function(instanceData) {
                        chooser.setState({
                            id: instanceData.pk,
                            display_title: instanceData.string
                        });
                    }
                }
            });
        }
    };

    chooserElement.find('.action-choose').click(function() {
        chooser.openChooserModal();
    });

    $('.action-clear', chooserElement).click(function() {
        chooser.clear();
    });

    return chooser;
};

/**
 * Singleton instance functioning as the public API for the ModelChooser
 */
window.wagtail.ui.ModelChooser = new ModelChooser();
})();

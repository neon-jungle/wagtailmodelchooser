function ModelChooser(id, opts) {
	/*
	id = the ID of the HTML element where chooser behaviour should be attached
	opts = dictionary of configuration options, which may include:
			modalWorkflowResponseName = the response identifier returned by the modal workflow to
					indicate that an item has been chosen. Defaults to 'chosen'.
	*/

	this.hooks = {
		setup: [],
		choose: [],
		ajax: [],
	};

	opts = opts || {};
	var self = this;

	this.id = id;
	this.chooserElement = $("#" + id + "-chooser");
	this.titleElement = this.chooserElement.find("[data-chooser-title]");
	this.previewElement = this.chooserElement.find("[data-chooser-preview]");
	this.imageElement = this.chooserElement.find("[data-chooser-image]");
	this.inputElement = $("#" + id);
	this.editLinkElement = this.chooserElement.find(".edit-link");
	this.editLinkWrapper = this.chooserElement.find(".edit-link-wrapper");
	if (!this.editLinkElement.attr("href")) {
		this.editLinkWrapper.hide();
	}
	this.chooseButton = $(".action-choose", this.chooserElement);
	this.idForLabel = null;
	this.baseModalURL = opts;

	this.baseModalUrl = this.chooserElement.data("chooser-url");

	this.modalResponses = {};
	this.modalResponses[opts.modalWorkflowResponseName || "chosen"] = function (data) {
		self.setStateFromModalData(data);
	};
	this.modalResponses["instanceChosen"] = function (data) {
		self.setStateFromModalData(data);
	};

	this.chooseButton.on("click", function () {
		self.openModal();
	});

	$(".action-clear", this.chooserElement).on("click", function () {
		self.setState(null);
	});

	// attach a reference to this widget object onto the root element of the chooser
	this.chooserElement.get(0).widget = this;
}

ModelChooser.prototype.getModalURL = function () {
	return this.baseModalURL;
};

ModelChooser.prototype.getModalURLParams = function () {
	return {};
};

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
ModelChooser.prototype.setupModal = function (modal, jsonData) {
	var that = this;

	/**
	 * Attach event handlers to the results. A live listener
	 * because we replace the modal contents with Ajax.
	 */
	modal.body.on("click", "a.model-choice", function (e) {
		e.preventDefault();
		var instance = $(this);

		// Call choose hooks
		for (var i = 0; i < that.hooks["choose"].length; i++) {
			var hook = that.hooks["choose"][i];

			// Allow mutation of params
			var result = hook.call(that, modal, instance);
			if (!result) {
				// Block choice
				return;
			}
		}

		var preview = null;
		if (instance.data("preview-url")) {
			preview = {
				url: instance.data("preview-url"),
				width: instance.data("preview-width"),
			};
		}

		modal.respond("instanceChosen", {
			string: instance.text(),
			pk: instance.data("pk"),
			preview: preview,
		});
		modal.close();
	});

	/**
	 * Handle pagination links. A live listener because we
	 * replace the modal content with Ajax.
	 */
	modal.body.on("click", ".pagination a", function (e) {
		e.preventDefault();
		var page = this.getAttribute("data-page");
		setPage(page);
	});

	/**
	 * Search the list
	 */
	var searchForm = modal.body.find("form.search-bar");
	var searchUrl = searchForm.attr("action");
	var searchResults = modal.body.find("#search-results");
	// Builds a dictionary of the values of fields in searchForm
	function buildSearchDict() {
		var rtn = {};
		searchForm.find("input, select, textarea").each(function () {
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
	$.each(that.hooks["setup"], function (_, hook) {
		hook.call(that, modal);
	});

	searchForm.submit(search);
	var searchChange = function (e) {
		clearTimeout($.data(this, "timer"));
		var wait = setTimeout(search, 250);
		$(this).data("timer", wait);
	};
	searchForm.on("input", searchChange);
	searchForm.on("change", searchChange);
	searchForm.on("keyup", searchChange);

	/**
	 * Load page number ``page`` of the results.
	 */
	function setPage(page) {
		loadResults(buildSearchDict(), page);
	}

	/**
	 * Actually do the work
	 */
	function loadResults(searchFields, page) {
		var dataObj = { ajax: 1 };
		if (window.instance) dataObj["instance"] = window.instance;
		if (page) dataObj["p"] = page;

		var params = $.extend(dataObj, searchFields);

		// Call ajax hooks
		for (var i = 0; i < that.hooks["ajax"].length; i++) {
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
			success: function (data, status) {
				searchResults.html(data);
			},
		});
	}
};

ModelChooser.prototype.openModal = function () {
	ModalWorkflow({
		url: this.getModalURL(),
		urlParams: this.getModalURLParams(),
		onload: {
			show_model_chooser: this.setupModal.bind(this),
		},
		responses: this.modalResponses,
	});
};

ModelChooser.prototype.setStateFromModalData = function (data) {
	this.setState({
		id: data.id || data.pk,
		title: data.string,
		preview: data.preview,
		edit_item_url: data.edit_link,
	});
};

ModelChooser.prototype.setState = function (newState) {
	if (newState && newState.id !== null && newState.id !== "") {
		this.inputElement.val(newState.id);
		this.titleElement.text(newState.title);
		this.chooserElement.removeClass("blank");
		if (newState.preview) {
			this.imageElement.attr("hidden", false);
			this.previewElement.attr("hidden", true);
			this.imageElement.attr("src", newState.preview.url);
			this.imageElement.attr("width", newState.preview.width);
		} else {
			this.imageElement.attr("hidden", true);
			this.previewElement.attr("hidden", false);
		}
		if (newState.edit_item_url) {
			this.editLinkElement.attr("href", newState.edit_item_url);
			this.editLinkWrapper.show();
		} else {
			this.editLinkWrapper.hide();
		}
	} else {
		this.inputElement.val("");
		this.chooserElement.addClass("blank");
	}
	this.inputElement.trigger("change");
};

ModelChooser.prototype.getState = function () {
	return {
		value: this.inputElement.val(),
		title: this.titleElement.text(),
		edit_item_url: this.editLinkElement.attr("href"),
	};
};

ModelChooser.prototype.getValue = function () {
	return this.inputElement.val();
};

ModelChooser.prototype.focus = function () {
	this.chooseButton.focus();
};

function ModelChooserFactory(html, opts) {
	this.html = html;
	this.opts = opts;
	this.widgetClass = ModelChooser;
}
ModelChooserFactory.prototype.render = function (placeholder, name, id, initialState, ...props) {
	var html = this.html.replace(/__NAME__/g, name).replace(/__ID__/g, id);
	placeholder.outerHTML = html;

	var chooser = new this.widgetClass(id, this.opts);
	chooser.setState(initialState);
	return chooser;
};
ModelChooserFactory.prototype.getModalURLParams = function () {
	return {};
};
ModelChooserFactory.prototype.openModal = function (callback, urlParams) {
	var responses = [];
	responses[this.opts.modalWorkflowResponseName || "chosen"] = callback;

	var fullURLParams = this.getModalURLParams();
	if (urlParams) {
		for (key in urlParams) {
			fullURLParams[key] = urlParams[key];
		}
	}
};
ModelChooserFactory.prototype.getById = function (id) {
	/* retrieve the widget object corresponding to the given HTML ID */
	return document.getElementById(id + "-chooser").widget;
};

window.ModelChooserFactory = ModelChooserFactory;

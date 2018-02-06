function createModelChooser(id, url) {
    var chooserElement = $('#' + id + '-chooser');
    var title = chooserElement.find('.title');
    var input = $('#' + id);

    chooserElement.find('.action-choose').click(function() {
        var modal = ModalWorkflow({
            url: url,
            responses: {
                instanceChosen: function(instanceData) {
                    input.val(instanceData.pk);
                    title.text(instanceData.string);
                    chooserElement.removeClass('blank');
                }
            }
        });
        modal.body.on("submit", "form", function (e) { e.preventDefault(); });
    });

    $('.action-clear', chooserElement).click(function() {
        input.val('');
        chooserElement.addClass('blank');
    });
}

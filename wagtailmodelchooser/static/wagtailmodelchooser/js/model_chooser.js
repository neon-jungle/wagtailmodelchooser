function createModelChooser(id, url) {
    var chooserElement = $('#' + id + '-chooser');
    var title = chooserElement.find('.title');
    var input = $('#' + id);

    chooserElement.find('.action-choose').click(function() {
        ModalWorkflow({
            url: url,
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

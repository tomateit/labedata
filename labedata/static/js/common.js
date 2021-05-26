function confirmedAction(question, actor) {
    (async function(event) {
        var confirmation = confirm(question);
        if (confirmation) {
            await actor();
        }
    })()
};
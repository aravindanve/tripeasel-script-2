// extracts pngs from output file
var page = new WebPage(),
    address = 'output.html', 
    outputDir = 'renders/';

page.viewportSize = { width: 1024, height: 1024 };

page.onConsoleMessage = function(msg, lineNum, sourceId) {
  console.log('> ' + msg);
};

page.open(address, function (status) {
    if (status !== 'success') {
        console.log('Unable to load the address!');
    } else 
    {   
        var clips = page.evaluate(function () {
            var clips = [], elems = document.querySelectorAll('.card');
            for (var i = 0; i < elems.length; i++) {
                var boundingRect = elems[i].getBoundingClientRect();
                clips.push({
                    top: boundingRect.top,
                    left: boundingRect.left,
                    width: boundingRect.width,
                    height: boundingRect.height
                });
                console.log('got card ' + (i + 1));
            }
            return clips;
        });

        var count = 1;

        for (var i = 0; i < clips.length; i++) {
            page.clipRect = clips[i];
            page.render(outputDir + 'card-' + count + '.png');
            console.log('saved card ' + (i + 1));
            count++;
        }

        phantom.exit();
  }
});



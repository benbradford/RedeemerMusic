var fs = require('fs');

var convert = (filename) => {
 fs.readFile(filename, function(err, data) {
     if (err) {
        console.error(err);
        return;
     }
    var splitLines = data.toString().split('\n');
    var slides = [];
    var lines = [];
    for (var line of splitLines) {
        if (line === "") {
            if (lines.length > 0) {
                slides.push(lines);
            }
            lines = [];
        } else {
            lines.push(line);
        }
    }
    var output = "{";
    var firstLine = true;
    if (slides.length > 0) {
        output += '\n';
        output += '  "slides": [\n';
        for (var slide of slides) {
            if (firstLine == false) {
                output += '    ,\n';
            }
            firstLine = false;
            output += '     [\n';
            var numLines = slide.length;
            var num = 0;
            for (var line of slide) {
                output += '     "' + line + '"';
                ++num;
                if (num < numLines) {
                    output +=',';
                }
                output +='\n';
            }
            output += '    ]\n';
        }
        output += '  ]\n';
    }
    output += "}";
    var outFile = filename.replace(".txt", ".json");

    fs.writeFileSync(outFile, output);
    console.log("written to " + outFile);
  });
};

convert("./ppt/Amazing Grace.txt");
/*
fs.readdir('./ppt/', function (err, files) {
  if (err) {
    console.error("Could not list the directory.", err);
    process.exit(1);
  }

  files.forEach(function (file, index) {
    convert("./ppt/" + file);
  });
});*/

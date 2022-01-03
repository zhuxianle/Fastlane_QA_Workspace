function removeJavaScriptDisabledWarning() {
    // Not using jQuery here for maximum speed
    document.getElementById('javascript-disabled').style.display = 'none';
}

function addJavaScriptDisabledWarning(error) {
    if (window.console)
        console.error('Opening failed: ' + error.name + ': ' + error.message);
    document.getElementById('javascript-disabled').style.display = 'block';
}

function initLayout(suiteName, type) {
    parseTemplates();
    setTitle(suiteName, type);
    addHeader();
    addReportOrLogLink(type);
}

function parseTemplates() {
    $('script[type="text/x-jquery-tmpl"]').map(function (idx, elem) {
        $.template(elem.id, elem.text);
    });
}

function setTitle(suiteName, type) {
    var givenTitle = window.settings.title;
    var title = givenTitle ? givenTitle : suiteName + " Test " + type;
    document.title = util.unescape(title);
}

function addHeader() {
    $.tmpl('<h1>${title}</h1>' +
           '<div id="generated">' +
             '<span>\u4ea7\u751f\u4e8e<br>${generated}</span><br>' +
             '<span id="generated-ago">${ago} \u4e4b\u524d</span>' +
           '</div>' +
           '<div id="top-right-header">' +
             '<div id="report-or-log-link"><a href="#"></a></div>' +
             '<div id="report-or-log-link2"><a href="#">\u6027\u80fd\u6d4b\u8bd5\u62a5\u544a</a></div>' +
           '</div>', {
        generated: window.output.generatedTimestamp,
        ago: util.createGeneratedAgoString(window.output.generatedMillis),
        title: document.title
    }).appendTo($('#header'));
}

function addReportOrLogLink(myType) {
    var url;
    var text;
    var container = $('#report-or-log-link');
    if (myType == 'Report') {
        url = window.settings.logURL;
        text = '\u529f\u80fd\u6d4b\u8bd5\u65e5\u5fd7';
    } else {
        url = window.settings.reportURL;
        text = '\u529f\u80fd\u6d4b\u8bd5\u62a5\u544a';
    }
    if (url) {
        container.find('a').attr('href', url);
        container.find('a').text(text);
    } else {
        container.remove();
    }
}

function addStatistics() {
    var statHeaders =
        '<th class="stats-col-stat">\u603b\u8ba1</th>' +
        '<th class="stats-col-stat">\u901a\u8fc7</th>' +
        '<th class="stats-col-stat">\u5931\u8d25</th>' +
        '<th class="stats-col-elapsed">\u8017\u65f6</th>' +
        '<th class="stats-col-graph">\u901a\u8fc7/\u5931\u8d25</th>';
    var statTable =
        '<h2>\u6d4b\u8bd5\u7edf\u8ba1</h2>' +
        '<table class="statistics" id="total-stats"><thead><tr>' +
        '<th class="stats-col-name">\u7ea7\u522b\u7edf\u8ba1</th>' + statHeaders +
        '</tr></thead></table>' +
        '<table class="statistics" id="tag-stats"><thead><tr>' +
        '<th class="stats-col-name">\u6807\u7b7e\u7edf\u8ba1</th>' + statHeaders +
        '</tr></thead></table>' +
        '<table class="statistics" id="suite-stats"><thead><tr>' +
        '<th class="stats-col-name">\u6d4b\u8bd5\u96c6\u7edf\u8ba1</th>' + statHeaders +
        '</tr></thead></table>';
    $(statTable).appendTo('#statistics-container');
    util.map(['total', 'tag', 'suite'], addStatTable);
    addTooltipsToElapsedTimes();
    enableStatisticsSorter();
}

function addTooltipsToElapsedTimes() {
    $('.stats-col-elapsed').attr('title',
        'Total execution time of these test cases. ' +
        'Excludes suite setups and teardowns.');
    $('#suite-stats').find('.stats-col-elapsed').attr('title',
        'Total execution time of this test suite.');
}

function enableStatisticsSorter() {
    $.tablesorter.addParser({
        id: 'statName',
        type: 'numeric',
        is: function(s) {
            return false;  // do not auto-detect
        },
        format: function(string, table, cell, cellIndex) {
            // Rows have class in format 'row-<index>'.
            var index = $(cell).parent().attr('class').substring(4);
            return parseInt(index);
        }
    });
    $(".statistics").tablesorter({
        sortInitialOrder: 'desc',
        headers: {0: {sorter:'statName', sortInitialOrder: 'asc'},
                  5: {sorter: false}}
    });
}

function addStatTable(tableName) {
    var stats = window.testdata.statistics()[tableName];
    if (tableName == 'tag' && stats.length == 0) {
        renderNoTagStatTable();
    } else {
        renderStatTable(tableName, stats);
    }
}

function renderNoTagStatTable() {
    $('<tbody><tr class="row-0">' +
        '<td class="stats-col-name">No Tags</td>' +
        '<td class="stats-col-stat"></td>' +
        '<td class="stats-col-stat"></td>' +
        '<td class="stats-col-stat"></td>' +
        '<td class="stats-col-elapsed"></td>' +
        '<td class="stats-col-graph">' +
          '<div class="empty-graph"></div>' +
        '</td>' +
      '</tr></tbody>').appendTo('#tag-stats');
}

function renderStatTable(tableName, stats) {
    var template = tableName + 'StatisticsRowTemplate';
    var tbody = $('<tbody></tbody>');
    for (var i = 0, len = stats.length; i < len; i++) {
        $.tmpl(template, stats[i], {index: i}).appendTo(tbody);
    }
    tbody.appendTo('#' + tableName + '-stats');
}

$.template('statColumnsTemplate',
    '<td class="stats-col-stat">${total}</td>' +
    '<td class="stats-col-stat">${pass}</td>' +
    '<td class="stats-col-stat">${fail}</td>' +
    '<td class="stats-col-elapsed">${elapsed}</td>' +
    '<td class="stats-col-graph">' +
      '{{if total}}' +
      '<div class="graph">' +
        '<div class="pass-bar" style="width: ${passWidth}%" title="${passPercent}%"></div>' +
        '<div class="fail-bar" style="width: ${failWidth}%" title="${failPercent}%"></div>' +
      '</div>' +
      '{{else}}' +
      '<div class="empty-graph"></div>' +
      '{{/if}}' +
    '</td>'
);

$.template('suiteStatusMessageTemplate',
    '${critical} critical test, ' +
    '${criticalPassed} passed, ' +
    '<span class="{{if criticalFailed}}fail{{else}}pass{{/if}}">${criticalFailed} failed</span><br>' +
    '${total} test total, ' +
    '${totalPassed} passed, ' +
    '<span class="{{if totalFailed}}fail{{else}}pass{{/if}}">${totalFailed} failed</span>'
);

// For complete cross-browser experience..
// http://www.quirksmode.org/js/events_order.html
function stopPropagation(event) {
    var event = event || window.event;
    event.cancelBubble = true;
    if (event.stopPropagation)
        event.stopPropagation();
}

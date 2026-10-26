// Google Apps Script — attached to "Metrifield — Website Enquiries".
// Receives POSTs from the website (contact form and chat assistant) and appends rows.
// Sheet 1 (first tab): contact-form enquiries.  Tab "Chat log": assistant Q&A.
function doPost(e) {
  var d = JSON.parse(e.postData.contents || "{}");
  var secret = PropertiesService.getScriptProperties().getProperty("SECRET");
  if (secret && d.secret !== secret) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false })).setMimeType(ContentService.MimeType.JSON);
  }
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var ts = Utilities.formatDate(new Date(), "Australia/Sydney", "yyyy-MM-dd HH:mm");
  if (d.kind === "chat") {
    var sh = ss.getSheetByName("Chat log");
    if (!sh) {
      sh = ss.insertSheet("Chat log");
      sh.appendRow(["Time (Sydney)", "Page", "Question", "Answer", "Status", "Sources", "Model"]);
      sh.setFrozenRows(1); sh.getRange(1, 1, 1, 7).setFontWeight("bold");
      sh.setColumnWidth(3, 320); sh.setColumnWidth(4, 480);
    }
    sh.appendRow([ts, d.page || "", d.question || "", d.answer || "", d.status || "", d.sources || "", d.model || ""]);
  } else {
    var sh1 = ss.getSheets()[0];
    sh1.appendRow([ts, d.name || "", d.org || "", d.email || "", d.type || "", d.msg || "", d.source || ""]);
  }
  return ContentService.createTextOutput(JSON.stringify({ ok: true })).setMimeType(ContentService.MimeType.JSON);
}

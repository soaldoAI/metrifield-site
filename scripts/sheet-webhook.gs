// Google Apps Script — attach to the "Metrifield — Website Enquiries" sheet.
// Extensions → Apps Script → paste this → Project Settings → Script properties:
//   SECRET = <same value as SHEET_WEBHOOK_SECRET in Cloudflare Pages>
// Deploy → New deployment → Web app → Execute as: Me; Who has access: Anyone → copy the URL
// into Cloudflare Pages secret SHEET_WEBHOOK_URL.
function doPost(e) {
  var d = JSON.parse(e.postData.contents || "{}");
  var secret = PropertiesService.getScriptProperties().getProperty("SECRET");
  if (!secret || d.secret !== secret) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false })).setMimeType(ContentService.MimeType.JSON);
  }
  var sh = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  var ts = Utilities.formatDate(new Date(), "Australia/Sydney", "yyyy-MM-dd HH:mm");
  sh.appendRow([ts, d.name || "", d.org || "", d.email || "", d.type || "", d.msg || "", d.source || ""]);
  return ContentService.createTextOutput(JSON.stringify({ ok: true })).setMimeType(ContentService.MimeType.JSON);
}

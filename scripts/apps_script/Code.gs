/**
 * SoundCave GTM — leads webhook (Google Apps Script).
 *
 * Container-bound to the "SoundCave GTM — Leads" sheet: open that sheet, then
 * Extensions > Apps Script, paste this file, save.
 *
 * Deploy: Deploy > New deployment > type "Web app" >
 *   Execute as:        Me
 *   Who has access:    Anyone
 * Copy the resulting /exec URL into the agent's SHEETS_WEBHOOK_URL.
 *
 * Optional auth: Project Settings > Script properties > add a property named
 * TOKEN with a random string, and set the same value in SHEETS_WEBHOOK_TOKEN so
 * only the agent can write.
 *
 * Accepts JSON POST bodies:
 *   { "action": "exists", "url": "<thread url>" }                 -> { "exists": bool }
 *   { "action": "create", "row": [ ...12 cells in HEADERS order ] } -> { "ok": true }
 *
 * The Python side (src/sinks/sheets.py) owns the column order and builds `row`;
 * this script just appends whatever array it is given.
 */

var URL_COLUMN = 9; // "Thread URL" is the 9th column

function doPost(e) {
  try {
    var body = JSON.parse(e.postData.contents);

    var wantToken = PropertiesService.getScriptProperties().getProperty('TOKEN');
    if (wantToken && body.token !== wantToken) {
      return _json({ error: 'unauthorized' });
    }

    var sheet = SpreadsheetApp.getActive().getSheets()[0];

    if (body.action === 'exists') {
      var lastRow = Math.max(sheet.getLastRow(), 1);
      var urls = sheet.getRange(1, URL_COLUMN, lastRow, 1).getValues();
      var found = false;
      for (var i = 0; i < urls.length; i++) {
        if (urls[i][0] === body.url) { found = true; break; }
      }
      return _json({ exists: found });
    }

    if (body.action === 'create') {
      sheet.appendRow(body.row);
      return _json({ ok: true });
    }

    return _json({ error: 'unknown action: ' + body.action });
  } catch (err) {
    return _json({ error: String(err) });
  }
}

function _json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

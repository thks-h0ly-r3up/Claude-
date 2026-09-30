/**
 * Shattering Chains - Google Sheets live sync webhook.
 *
 * Setup (see README):
 *  1. Create a Google Sheet, open Extensions > Apps Script, paste this file.
 *  2. Project Settings > Script properties > add WEBHOOK_SECRET = a long random string
 *     (the same value goes in Vercel as SHEETS_WEBHOOK_SECRET).
 *  3. Run setup() once (authorize when prompted).
 *  4. Deploy > New deployment > Web app > Execute as: Me, Who has access: Anyone.
 *     Copy the Web app URL into Vercel as SHEETS_WEBHOOK_URL.
 *
 * Requests are JSON POSTs: { secret, action: "upsert" | "update", ... }.
 */

var LEADS_SHEET = 'Leads';
var METRICS_SHEET = 'Metrics';
var HEADERS = ['Timestamp', 'Lead ID', 'Name', 'Email', 'Social Handle', 'Source Platform', 'PDF Downloaded', 'App Clicked'];
var COL = { TIMESTAMP: 1, ID: 2, NAME: 3, EMAIL: 4, HANDLE: 5, SOURCE: 6, PDF: 7, APP: 8 };

function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    var data = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    var secret = PropertiesService.getScriptProperties().getProperty('WEBHOOK_SECRET');
    if (!secret || !safeEqual_(String(data.secret || ''), secret)) {
      return json_({ ok: false, error: 'unauthorized' });
    }
    lock.waitLock(20000);
    var sheet = getLeadsSheet_();
    var action = data.action || 'upsert';

    if (action === 'upsert') {
      if (!data.id || !data.email) return json_({ ok: false, error: 'id and email required' });
      var row = findRow_(sheet, data.id, data.email);
      var values = [
        data.timestamp ? new Date(data.timestamp) : new Date(),
        String(data.id),
        String(data.name || ''),
        String(data.email).toLowerCase(),
        String(data.social_handle || ''),
        String(data.source_platform || 'direct'),
        data.pdf_downloaded === true,
        data.app_clicked === true
      ];
      if (row) {
        // Existing lead re-opted in: refresh contact fields, keep funnel flags that are already TRUE.
        var existing = sheet.getRange(row, 1, 1, HEADERS.length).getValues()[0];
        values[COL.TIMESTAMP - 1] = existing[COL.TIMESTAMP - 1] || values[COL.TIMESTAMP - 1];
        values[COL.PDF - 1] = existing[COL.PDF - 1] === true || values[COL.PDF - 1];
        values[COL.APP - 1] = existing[COL.APP - 1] === true || values[COL.APP - 1];
        sheet.getRange(row, 1, 1, HEADERS.length).setValues([values]);
      } else {
        sheet.appendRow(values);
      }
      return json_({ ok: true, action: 'upsert', row: row || sheet.getLastRow() });
    }

    if (action === 'update') {
      var target = findRow_(sheet, data.id, null);
      if (!target) return json_({ ok: false, error: 'lead not found' });
      var fields = data.fields || {};
      if (fields.pdf_downloaded === true) sheet.getRange(target, COL.PDF).setValue(true);
      if (fields.app_clicked === true) sheet.getRange(target, COL.APP).setValue(true);
      return json_({ ok: true, action: 'update', row: target });
    }

    return json_({ ok: false, error: 'unknown action' });
  } catch (err) {
    return json_({ ok: false, error: String(err && err.message ? err.message : err) });
  } finally {
    try { lock.releaseLock(); } catch (ignore) {}
  }
}

/** Health check: opening the URL in a browser shows the endpoint is live (no data exposed). */
function doGet() {
  return json_({ ok: true, service: 'shattering-chains-sheet-sync' });
}

/** Run once from the editor. Builds the Leads sheet, checkboxes, and a live Metrics dashboard. */
function setup() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var leads = getLeadsSheet_();

  leads.getRange(1, 1, 1, HEADERS.length)
    .setFontWeight('bold').setBackground('#0B1320').setFontColor('#FFB833');
  leads.setFrozenRows(1);
  leads.getRange('A2:A').setNumberFormat('yyyy-mm-dd hh:mm:ss');
  leads.getRange('G2:H10000').insertCheckboxes();
  leads.setColumnWidths(1, 1, 150);
  leads.setColumnWidths(2, 1, 250);
  leads.setColumnWidths(3, 1, 150);
  leads.setColumnWidths(4, 1, 240);
  leads.setColumnWidths(5, 1, 150);
  leads.setColumnWidths(6, 1, 130);
  leads.setColumnWidths(7, 2, 120);

  var metrics = ss.getSheetByName(METRICS_SHEET) || ss.insertSheet(METRICS_SHEET);
  metrics.clear();
  var rows = [
    ['Metric', 'Value'],
    ['Total leads', '=COUNTA(Leads!B2:B)'],
    ['Leads today', '=COUNTIFS(Leads!A2:A,">="&TODAY())'],
    ['Leads last 7 days', '=COUNTIFS(Leads!A2:A,">="&(TODAY()-7))'],
    ['PDF downloads', '=COUNTIF(Leads!G2:G,TRUE)'],
    ['App link clicks', '=COUNTIF(Leads!H2:H,TRUE)'],
    ['PDF download rate', '=IFERROR(B5/B2,0)'],
    ['App click rate', '=IFERROR(B6/B2,0)']
  ];
  metrics.getRange(1, 1, rows.length, 2).setValues(rows);
  metrics.getRange('A1:B1').setFontWeight('bold').setBackground('#0B1320').setFontColor('#FFB833');
  metrics.getRange('B7:B8').setNumberFormat('0.0%');
  metrics.getRange('D1').setValue('Leads by source').setFontWeight('bold');
  metrics.getRange('D2').setFormula(
    '=IFERROR(QUERY(Leads!A2:H,"select F, count(B) where F is not null group by F order by count(B) desc label F \'Source\', count(B) \'Leads\'",0),"No leads yet")'
  );
  metrics.setColumnWidth(1, 330);
  metrics.setColumnWidth(2, 110);
  metrics.setColumnWidth(4, 140);
  SpreadsheetApp.flush();
}

function getLeadsSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(LEADS_SHEET);
  if (!sheet) {
    sheet = ss.insertSheet(LEADS_SHEET);
  }
  if (sheet.getLastRow() === 0) {
    sheet.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
  }
  return sheet;
}

/** Returns the 1-based row of a lead by id (or email fallback), or 0 if absent. */
function findRow_(sheet, id, email) {
  var last = sheet.getLastRow();
  if (last < 2) return 0;
  var ids = sheet.getRange(2, COL.ID, last - 1, 1).getValues();
  for (var i = 0; i < ids.length; i++) {
    if (id && String(ids[i][0]) === String(id)) return i + 2;
  }
  if (email) {
    var emails = sheet.getRange(2, COL.EMAIL, last - 1, 1).getValues();
    var wanted = String(email).toLowerCase();
    for (var j = 0; j < emails.length; j++) {
      if (String(emails[j][0]).toLowerCase() === wanted) return j + 2;
    }
  }
  return 0;
}

function safeEqual_(a, b) {
  if (a.length !== b.length) return false;
  var diff = 0;
  for (var i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

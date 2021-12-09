function sortAndSend() {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheets()[0];
    var range = sheet.getRange("A:H");

    if (!range.isBlank()) {
        range.sort(7);

        MailApp.sendEmail({
            to: "okan@analyticahouse.com",
            subject: 'Product Report from Osman Arda Yýlmazer',
            htmlBody: "Here is the report<br><br>" +
                "https://docs.google.com/spreadsheets/d/10NQXE9iovumhJN5kd9jPrfQAMQWMH_ir_hs7Wwb8Zak\n<br><br>" +
                "Best Regards,"
        });
    }
}
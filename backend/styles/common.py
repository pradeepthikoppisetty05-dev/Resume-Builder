def common_styles():
    return """
    <style>
    @page {
        size: A4;
        margin: 20mm;
    }

    body {
        margin: 0;
        font-family: Arial, sans-serif;
    }

    .resume {
        width: 210mm;
        min-height: 297mm;
        padding: 20mm;
        box-sizing: border-box;
        background: white;
    }

    .section {
        margin-bottom: 16px;
        page-break-inside: avoid;
    }

    h1, h2 {
        margin: 0 0 8px 0;
    }
    </style>
    """

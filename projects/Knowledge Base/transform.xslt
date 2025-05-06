<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html" encoding="UTF-8" indent="yes"/>

  <!-- Match the root element -->
  <xsl:template match="/root">
    <html>
      <head>
        <!-- Use the XML title for the HTML title -->
        <title><xsl:value-of select="title"/></title>
        <style>
          /* You can even embed some basic CSS here or link externally */
          body { font-family: sans-serif; padding: 20px; }
        </style>
      </head>
      <body>
        <!-- Process the children of the root element -->
        <xsl:apply-templates/>
      </body>
    </html>
  </xsl:template>

  <!-- Match the title element (already used for <title>, maybe display as h1?) -->
  <xsl:template match="title">
     <h1><xsl:value-of select="."/></h1>
  </xsl:template>

  <!-- Match h1 elements and output HTML h1 -->
  <xsl:template match="h1">
    <h1><xsl:apply-templates/></h1>
  </xsl:template>

  <!-- Match h2 elements and output HTML h2 -->
  <xsl:template match="h2">
    <h2><xsl:apply-templates/></h2>
  </xsl:template>

</xsl:stylesheet>

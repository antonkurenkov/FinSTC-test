<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output method="html" indent="yes" encoding="utf-8" doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN"/>
<xsl:template match="/">
<person>
    <name><xsl:value-of select="./person/name" /></name>
    <surname><xsl:value-of select="./person/surname" /></surname>
    <age><xsl:value-of select="./person/age" /></age>
</person>
</xsl:template>
</xsl:stylesheet>
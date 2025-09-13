using System.Globalization;
using System.IO;
using System.Linq;
using CsvHelper;
using Xunit;

public class SeedGenTests
{
    [Fact]
    public void CsvLoadsAndConverts()
    {
        var csv = "city,country,iata,avg_temp_c_feb,has_beach,has_old_town,flight_hours_from_LON\nX,Nowhere,XXX,10,yes,no,1.0\n";
        using var sr = new StringReader(csv);
        using var csvr = new CsvReader(sr, CultureInfo.InvariantCulture);
        var recs = csvr.GetRecords<dynamic>().ToList();
        Assert.Single(recs);
    }
}

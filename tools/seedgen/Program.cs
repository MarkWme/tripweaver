using System.Globalization;
using System.Text.Json;
using CsvHelper;

var csvPathEnv = Environment.GetEnvironmentVariable("CSV_PATH");
string csvPath;
if (!string.IsNullOrEmpty(csvPathEnv))
{
    csvPath = csvPathEnv!;
}
else
{
    // Prefer mounted /app/data when running in the container
    var candidate1 = Path.Combine(AppContext.BaseDirectory, "data", "destinations.csv");
    var candidate2 = Path.Combine(AppContext.BaseDirectory, "../../../../data/destinations.csv");
    if (File.Exists(candidate1)) csvPath = candidate1;
    else csvPath = candidate2;
}

if (!File.Exists(csvPath))
{
    Console.WriteLine($"CSV not found at {csvPath}");
    return 1;
}

using var reader = new StreamReader(csvPath);
using var csv = new CsvReader(reader, CultureInfo.InvariantCulture);
var records = csv.GetRecords<dynamic>().ToList();

var list = new List<object>();
foreach (var r in records)
{
    var dict = new Dictionary<string, object?>();
    foreach (var kv in (IDictionary<string, object?>)r)
    {
        dict[kv.Key] = kv.Value;
    }
    list.Add(dict);
}

var index = new
{
    generated_at = DateTime.UtcNow.ToString("o"),
    count = list.Count,
    destinations = list
};

var outDir = Path.Combine(AppContext.BaseDirectory, "../../../../data");
Directory.CreateDirectory(outDir);
var outPath = Path.Combine(outDir, "index.json");
var json = JsonSerializer.Serialize(index, new JsonSerializerOptions { WriteIndented = true });
File.WriteAllText(outPath, json);
Console.WriteLine($"Wrote {outPath}");
return 0;

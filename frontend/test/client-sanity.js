// simple offline sanity test (no external deps)
const assert = require('assert');
const s = '{"origin":"LON","when":"next week","prefs":["warm"],"max_flight_hours":2}';
const obj = JSON.parse(s);
assert.strictEqual(obj.origin, 'LON');
console.log('frontend sanity test passed');

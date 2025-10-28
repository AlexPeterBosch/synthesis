# Phase 7 Validation

## Node Sizing Test

```javascript
// CRITICAL: Must be LINEAR
const size = 5 + (bc_normalized * 35);

// NOT logarithmic!
// DON'T use: Math.log(bc) * scale
```

## Performance Test

- [ ] 500 nodes: smooth (60 FPS)
- [ ] 1000 nodes: acceptable (30+ FPS)
- [ ] Zoom responsive
- [ ] Pan smooth

## Success Criteria

Visualization matches specifications exactly.
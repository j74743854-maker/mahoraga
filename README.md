# Rueda de Adaptación de Mahoraga — Fabric, Minecraft Java 26.3

## Cómo funciona
- Te adaptas a **cualquier tipo de daño** (14 categorías: fuego y lava, ahogamiento, asfixia, caída, explosión, proyectiles, golpes, magia, contacto, objetos que caen, congelación, rayos, hambre, otros). El vacío y `/kill` no son adaptables.
- Cada tipo tiene 3 fases (golpes necesarios: 1 / 3 / 6, editable en `AdaptationData.THRESHOLDS`):
  - **1/3** cura el 40 % del daño recibido · **2/3** cura el 150 % · **3/3** inmunidad total (el daño se cancela; en fuego dejas de arder y en ahogamiento respiras bajo el agua).
- Se aprende de todo lo que te golpea, pero **solo una adaptación activa a la vez**. Con **R** abres el menú radial y eliges cuál activar (clic en el centro = desactivar). La primera que desbloqueas se activa sola.
- La rueda 3D flota sobre tu cabeza (la ven los demás jugadores), gira 45° con cada adaptación con un pequeño rebote, y su gema toma el color de la adaptación activa.
- Los datos se guardan en el jugador y se conservan al morir.

## Compilar
Requiere JDK 25 y Gradle 9.x (o copia el wrapper de la plantilla oficial de Fabric).
```
gradle wrapper        # una sola vez, si no tienes gradlew
./gradlew runClient   # probar en desarrollo
./gradlew build       # jar en build/libs/
```
Instala el jar en `mods/` junto a Fabric Loader 0.20.1+ y Fabric API 0.165+ para 26.3. Funciona en servidor (lógica) y cliente (menú y rueda).

## Puntos de la API de 26.x que conviene revisar si el compilador se queja
Mojang renombró mucho entre 26.1 y 26.3. Están todos aislados en estos sitios:
- `AdaptationScreen`: `GuiGraphicsExtractor` (`text`, `centeredText`, `item`, `blit` con color), `MouseButtonEvent`, `KeyEvent`.
- `WheelLayer`: `RenderTypes.entityCutoutNoCull`, `submitCustomGeometry`, `AvatarRenderer`/`AvatarRenderState`.
- `MahoragaClient`: `KeyMappingHelper` y `KeyMapping.Category`.
- `Compat`: abrir pantallas (resuelto por reflexión).
- `MahoragaMod`: `PayloadTypeRegistry.serverboundPlay()`.

`gen_textures.py` regenera las 4 texturas (requiere Pillow).

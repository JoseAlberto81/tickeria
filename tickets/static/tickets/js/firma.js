window.addEventListener('DOMContentLoaded', function() {
    var canvas = document.getElementById('firma-canvas');
    if (canvas) {
        var signaturePad = new SignaturePad(canvas);

        window.limpiarFirma = function() {
            signaturePad.clear();
        };

        window.guardarFirma = function() {
            if (!signaturePad.isEmpty()) {
                document.getElementById('firma_data').value = signaturePad.toDataURL();
            }
        };
    }
});
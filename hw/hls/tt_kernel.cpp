#include <ap_int.h>
#include <hls_stream.h>

struct AxisWord {
    ap_uint<32> data;
    ap_uint<1> last;
};

// Skeleton de kernel de contracción TT.
// - in_stream: activaciones de entrada (AXI-Stream)
// - out_stream: resultados (AXI-Stream)
// - cores_ptr: DDR con cores TT linealizados
// - dims/ranks: metadatos de tamaño
// - ctrl: registros de control (no modelados aquí)
void tt_kernel(
    hls::stream<AxisWord> &in_stream,
    hls::stream<AxisWord> &out_stream,
    const ap_int<16> *cores_ptr,
    const ap_uint<32> *dims,
    const ap_uint<32> *ranks,
    const ap_uint<32> *ctrl
) {
#pragma HLS INTERFACE axis port=in_stream
#pragma HLS INTERFACE axis port=out_stream
#pragma HLS INTERFACE m_axi depth=4096 port=cores_ptr offset=slave bundle=gmem
#pragma HLS INTERFACE m_axi depth=64 port=dims offset=slave bundle=gmem
#pragma HLS INTERFACE m_axi depth=64 port=ranks offset=slave bundle=gmem
#pragma HLS INTERFACE s_axilite port=ctrl bundle=control
#pragma HLS INTERFACE s_axilite port=return bundle=control

    // Supuestos:
    // - Q1.14 para pesos/activaciones.
    // - Acumulador interno en 32 bits con saturación.
    // - Cores TT en layout (r_in, n_out, n_in, r_out) linealizado.

    // Placeholder: leer configuración básica.
    ap_uint<32> d0 = dims[0];
    ap_uint<32> r0 = ranks[0];

    // Pipeline de consumo/producción de stream.
    // En implementación real, aquí se realiza la contracción TT.
    AxisWord in_word;
    AxisWord out_word;

    // Bucle representativo de streaming.
    for (ap_uint<32> i = 0; i < d0; ++i) {
#pragma HLS PIPELINE II=1
        if (!in_stream.empty()) {
            in_word = in_stream.read();
            // Acceso representativo a core TT.
            ap_int<16> w = cores_ptr[(r0 + i) & 0xFFF];
            ap_int<32> acc = (ap_int<32>)w * (ap_int<16>)in_word.data.range(15, 0);
            // Saturación simple a 16 bits.
            ap_int<16> y = (acc > 32767) ? 32767 : (acc < -32768) ? -32768 : (ap_int<16>)acc;

            out_word.data = (ap_uint<32>)y;
            out_word.last = in_word.last;
            out_stream.write(out_word);
        }
    }
}

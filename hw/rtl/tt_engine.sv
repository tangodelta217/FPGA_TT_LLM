// Skeleton RTL para TT Contraction Engine.
module tt_engine (
    input  logic         clk,
    input  logic         rst_n,

    // AXI-Stream input
    input  logic [31:0]  s_axis_tdata,
    input  logic         s_axis_tvalid,
    output logic         s_axis_tready,
    input  logic         s_axis_tlast,

    // AXI-Stream output
    output logic [31:0]  m_axis_tdata,
    output logic         m_axis_tvalid,
    input  logic         m_axis_tready,
    output logic         m_axis_tlast,

    // Simple counters for observability
    output logic [31:0]  cycles,
    output logic [31:0]  stalls
);

    // Pipeline registers
    logic [31:0] data_reg;
    logic        last_reg;

    // Counters for "wow"
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            cycles <= 32'd0;
            stalls <= 32'd0;
        end else begin
            cycles <= cycles + 1;
            if (s_axis_tvalid && !s_axis_tready) begin
                stalls <= stalls + 1;
            end
        end
    end

    // Input readiness: simple backpressure from output
    assign s_axis_tready = m_axis_tready || !m_axis_tvalid;

    // Simple pass-through pipeline stage
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            m_axis_tvalid <= 1'b0;
            m_axis_tdata  <= 32'd0;
            m_axis_tlast  <= 1'b0;
            data_reg      <= 32'd0;
            last_reg      <= 1'b0;
        end else begin
            if (s_axis_tvalid && s_axis_tready) begin
                // Placeholder: aqui iria MAC y acumulacion TT.
                data_reg <= s_axis_tdata;
                last_reg <= s_axis_tlast;
                m_axis_tvalid <= 1'b1;
            end else if (m_axis_tready) begin
                m_axis_tvalid <= 1'b0;
            end

            if (m_axis_tvalid && m_axis_tready) begin
                m_axis_tdata <= data_reg;
                m_axis_tlast <= last_reg;
            end
        end
    end

endmodule

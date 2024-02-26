import React from "react";
import ApexCharts from "react-apexcharts";

function Chart() {
  return (
    <ApexCharts
      type="area"
      series={[
        {
          name: "winning rate blue",
          data: [
            { x: 1996, y: 100 },
            { x: 1997, y: 90 },
            { x: 1998, y: 50 },
            { x: 1999, y: 77 },
            { x: 2000, y: 35 },
            { x: 2001, y: 0 },
            { x: 2002, y: 0 },
            { x: 2003, y: 0 },
            { x: 2004, y: 0 },
            { x: 2005, y: 0 },
            { x: 2006, y: 0 },
            { x: 2007, y: 0 },
            { x: 2008, y: 0 },
            { x: 2009, y: 0 },
            { x: 2010, y: 0 },
            { x: 2011, y: 0 },
            { x: 2012, y: 0 },
            { x: 2013, y: 33 },
            { x: 2014, y: 54 },
            { x: 2015, y: 60 },
          ],
        },
        {
          name: "winning rate red",
          data: [
            { x: 1996, y: 0 },
            { x: 1997, y: 0 },
            { x: 1998, y: 0 },
            { x: 1999, y: 0 },
            { x: 2000, y: 0 },
            { x: 2001, y: 0 },
            { x: 2002, y: -32 },
            { x: 2003, y: -40 },
            { x: 2004, y: -49 },
            { x: 2005, y: -41 },
            { x: 2006, y: -32 },
            { x: 2007, y: -27 },
            { x: 2008, y: -22 },
            { x: 2009, y: -18 },
            { x: 2010, y: -22 },
            { x: 2011, y: -33 },
            { x: 2012, y: 0 },
            { x: 2013, y: 0 },
            { x: 2014, y: 0 },
            { x: 2015, y: 0 },
          ],
        },
      ]}
      options={{
        plotOptions: {
          area: {
            fillTo: "origin",
          },
        },
        colors: ["#5E82E1", "#D64E5B"],
        theme: {
          mode: "dark",
        },
        chart: {
          type: "area",
          width: "100%",
          height: 400,
          background: "transparent",
          toolbar: {
            show: false,
          },
        },
        markers: {
          shape: "rect",
        },

        dataLabels: {
          enabled: false,
        },
        stroke: {
          colors: ["#D64E5B", "#5E82E1"],
          width: 0,
          curve: "smooth",
        },
        title: {
          text: "",
          align: "left",
          style: {
            fontSize: "14px",
          },
        },
        xaxis: {
          tooltip: {
            enabled: false,
          },
          type: "datetime",
          axisBorder: {
            show: false,
          },
          axisTicks: {
            show: false,
          },
        },
        yaxis: {
          tickAmount: 4,
          floating: false,
          min: -100,
          max: 100,
          forceNiceScale: false,
          labels: {
            style: {
              colors: "#8e8da4",
            },
            offsetY: -7,
            offsetX: 0,
            formatter: function (value) {
              return Math.abs(value).toString();
            },
          },
          axisBorder: {
            show: false,
          },
          axisTicks: {
            show: false,
          },
        },

        fill: { type: "solid", opacity: 0.5 },

        tooltip: {
          x: {},
          custom: function ({ series, seriesIndex, dataPointIndex, w }) {
            const yValue = Math.abs(
              w.globals.initialSeries[seriesIndex].data[dataPointIndex].y
            );
            const xValue =
              w.globals.initialSeries[seriesIndex].data[dataPointIndex].x;
            if (yValue !== 0) {
              return (
                "<div style='background-color: #090A0B; color: #fff; padding: 10px; font-size: 12px; font-weight: 600;'>" +
                xValue +
                ": " +
                yValue +
                "</div>"
              );
            } else {
              return "";
            }
          },
        },
        grid: {
          yaxis: {
            lines: {
              show: false,
              offsetX: -30,
            },
          },
          padding: {
            left: 20,
          },
        },
      }}
    />
  );
}

export default Chart;

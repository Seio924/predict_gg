import { createGlobalStyle } from "styled-components";
import PretendardBlack from "./fonts/Pretendard-Black.woff2";
import PretendardBold from "./fonts/Pretendard-Bold.woff2";
import PretendardExtraBold from "./fonts/Pretendard-ExtraBold.woff2";
import PretendardExtraLight from "./fonts/Pretendard-ExtraLight.woff2";
import PretendardLight from "./fonts/Pretendard-Light.woff2";
import PretendardMedium from "./fonts/Pretendard-Medium.woff2";
import PretendardRegular from "./fonts/Pretendard-Regular.woff2";
import PretendardSemiBold from "./fonts/Pretendard-SemiBold.woff2";

const GlobalStyle = createGlobalStyle`
@font-face {
        font-family: 'PretendardBlack';
        font-style: normal;
        src: url(${PretendardBlack}) format('woff2');
  }
  @font-face {
        font-family: 'PretendardBold';
        font-style: normal;
        src: url(${PretendardBold}) format('woff2');
  }
  @font-face {
        font-family: 'PretendardMedium';
        font-style: normal;
        src: url(${PretendardMedium}) format('woff2');
  }
  @font-face {
        font-family: 'PretendardSemiBold';
        font-style: normal;
        src: url(${PretendardSemiBold}) format('woff2');
  }
html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
del, dfn, em, img, ins, kbd, q, s, samp,
small, strike, strong, sub, sup, tt, var,
b, u, i, center,
dl, dt, dd, ol, ul, li,
fieldset, form, label, legend,
table, caption, tbody, tfoot, thead, tr, th, td,
article, aside, canvas, details, embed, 
figure, figcaption, footer, header, hgroup, 
menu, nav, output, ruby, section, summary,
time, mark, audio, video {
	margin: 0;
	padding: 0;
	border: 0;
	font-size: 100%;
	font: inherit;
	vertical-align: baseline;
}
/* HTML5 display-role reset for older browsers */
article, aside, details, figcaption, figure, 
footer, header, hgroup, menu, nav, section {
	display: block;
}
html, body, #root {
	line-height: 1;
    height: 100%;
}
ol, ul {
	list-style: none;
}
blockquote, q {
	quotes: none;
}
blockquote:before, blockquote:after,
q:before, q:after {
	content: '';
	content: none;
}
table {
	border-collapse: collapse;
	border-spacing: 0;
}
`;

export default GlobalStyle;

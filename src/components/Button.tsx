import styled, { css } from "styled-components";

const defaultBackgroundColor = css`
  background-color: rgba(0, 0, 0, 0);
  border: 1px solid #ffffff;
`;

const firstColorBackground = css`
  background-image: linear-gradient(
    265deg,
    rgba(24, 200, 255, 0.7),
    rgba(147, 63, 254, 0.7)
  );
`;

const secondColorBackground = css`
  background-image: linear-gradient(
    265deg,
    rgba(198, 197, 197, 0.7),
    rgba(91, 90, 90, 0.7)
  );
`;

const Btn = styled.div<{ btnColor?: boolean }>`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 45px;
  width: 100%;
  border-radius: 7px;
  margin-top: 15px;
  cursor: pointer;
  ${(props) =>
    props.btnColor === true
      ? firstColorBackground
      : props.btnColor === false
      ? secondColorBackground
      : defaultBackgroundColor};
  &:first-child {
    margin-right: 18px;
  }
`;

const BtnText = styled.p`
  font-size: 20px;
  font-weight: 600;
  color: #eeeeef;
`;

interface IProps {
  btnColor?: boolean;
  onClick: () => void;
  children?: React.ReactNode;
}

function Button({ btnColor, onClick, children }: IProps) {
  return (
    <>
      <Btn btnColor={btnColor} onClick={onClick}>
        <BtnText>{children}</BtnText>
      </Btn>
    </>
  );
}

export default Button;

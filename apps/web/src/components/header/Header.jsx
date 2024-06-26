import { Button } from "@consta/uikit/Button";
import { Layout } from "@consta/uikit/Layout";
import { Text } from "@consta/uikit/Text";
import { Link } from "react-router-dom";
const Header = () => {
  return (
    <Layout
      flex={1}
      className="header"
      style={{
        justifyContent: "space-between",
        alignItems: "center",
        maxHeight: "60px",
      }}
    >
      <Text view="primary" size="m" lineHeight="m" style={{ padding: "0px" }}>
        <Link to="/" style={{ textDecoration: "none" }}>
          <img src="/logo.png" alt="" className="logo" />
        </Link>
      </Text>
      <Link to="/add" style={{ textDecoration: "none" }}>
        <Button label="Добавить видео" className="btn_white" />
      </Link>
    </Layout>
  );
};

export default Header;

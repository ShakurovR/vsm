import { Layout } from "@consta/uikit/Layout";
import { Text } from "@consta/uikit/Text";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <Layout flex={1}>
      <Text view="primary" size="m" lineHeight="m">
        <Link to="/">HEADER</Link>
      </Text>
    </Layout>
  );
};

export default Header;

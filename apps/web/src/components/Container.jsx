import { Grid } from "@consta/uikit/Grid";
import PropTypes from "prop-types";
import { EqualHeight } from "react-equal-height";
const Container = ({ children }) => {
  return (
    <Grid
      cols={1}
      xAlign="center"
      gap="xl"
      style={{ marginTop: "30px" }}
      breakpoints={{
        768: {
          cols: 3,
        },
      }}
    >
      <EqualHeight>{children}</EqualHeight>
    </Grid>
  );
};
Container.propTypes = {
  children: PropTypes.node.isRequired,
};
export default Container;

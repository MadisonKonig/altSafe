import Container from "react-bootstrap/Container";
import BootstrapNav from "react-bootstrap/Nav";
import BootstrapNavbar from "react-bootstrap/Navbar";

function Navbar() {
  return (
    <BootstrapNavbar expand="lg" className="bg-body-tertiary">
      <Container>
        <BootstrapNavbar.Brand href="#home">App</BootstrapNavbar.Brand>
        <BootstrapNavbar.Toggle aria-controls="basic-navbar-nav" />
        <BootstrapNavbar.Collapse id="basic-navbar-nav">
          <BootstrapNav className="me-auto">
            <BootstrapNav.Link href="#home">Home</BootstrapNav.Link>
            <BootstrapNav.Link href="#link">Link</BootstrapNav.Link>
          </BootstrapNav>
        </BootstrapNavbar.Collapse>
      </Container>
    </BootstrapNavbar>
  );
}

export default Navbar;
